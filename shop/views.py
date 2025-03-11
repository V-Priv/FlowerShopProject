from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import RegisterForm, UserLoginForm, OrderForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Flower, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .telegram_bot import send_order_confirmation
from django.contrib import messages

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'shop/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

def home(request):
    return render(request, 'shop/home.html')

@login_required(login_url='/register/')
def catalog(request):
    flowers = Flower.objects.filter(available=True)
    return render(request, 'shop/catalog.html', {'flowers': flowers})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'shop/register.html', {'form': form})

@login_required
def create_order(request):
    flowers = Flower.objects.all()
    if request.method == "POST":
        form = OrderForm(flowers, request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for flower in flowers:
                quantity = form.cleaned_data.get(f'quantity_{flower.id}', 0)
                if quantity > 0:
                    OrderItem.objects.create(order=order, flower=flower, quantity=quantity)

            return redirect('order_detail', order_id=order.id)

    else:
        form = OrderForm(flowers)

    return render(request, 'shop/order.html', {'form': form, 'flowers': flowers})


@require_POST
@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    try:
        send_order_confirmation(order)
        messages.success(request, "✅ Заказ подтвержден! Уведомление отправлено администратору.")
    except Exception as e:
        messages.error(request, f"❌ Ошибка отправки уведомления: {str(e)}")

    return redirect('order_confirmation')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def order_confirmation(request):
    return render(request, 'shop/order_confirmation.html')

def logout_view(request):
    logout(request)
    return redirect('home')


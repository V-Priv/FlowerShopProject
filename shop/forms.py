from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    def __init__(self, flowers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flowers = flowers
        for flower in flowers:
            self.fields[f'quantity_{flower.id}'] = forms.IntegerField(
                min_value=0,
                initial=0,
                required=False,
                label=f'Количество {flower.name}'
            )

    delivery_address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите адрес доставки'}),
        label="Адрес доставки"
    )

    delivery_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'placeholder': 'Введите дату и время доставки'}),
        label="Дата и время доставки"
    )

    class Meta:
        model = Order
        fields = ["delivery_address", "delivery_datetime"]  # Добавляйте здесь другие необходимые поля

    def save(self, commit=True):
        order = super().save(commit=False)
        total_price = 0
        for flower in self.flowers:
            quantity = self.cleaned_data.get(f'quantity_{flower.id}', 0)
            total_price += quantity * flower.price
            # Здесь можно добавить логику для создания связанного объекта
            # Например, если Order имеет связь с Quantity:
            # order.flowers.create(flower=flower, quantity=quantity)

        order.total_price = total_price  # Если у вас есть поле total_price в модели Order
        if commit:
            order.save()
        return order

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))



class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Электронная почта"),
        help_text=_("Пожалуйста, укажите ваш действующий адрес электронной почты."),
        widget=forms.EmailInput(attrs={'placeholder': 'example@domain.com'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            'username': _("Имя пользователя"),
            'password1': _("Пароль"),
            'password2': _("Подтверждение пароля"),
        }
        help_texts = {
            'username': _("Обязательное поле. Максимум 150 символов. Разрешены буквы, цифры и символы @/./+/-/_."),
            'password1': _("Пароль может быть простым. Минимум 4 символа.")
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _(
            "Ваш пароль может быть простым. Минимум 4 символа."
        )
        self.fields['password2'].help_text = _(
            "Введите тот же пароль для проверки."
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # Убираем все проверки, кроме минимальной длины (если она вам нужна)
        if len(password1) < 4:
            raise forms.ValidationError(_("Пароль должен содержать минимум 4 символа."))
        return password1

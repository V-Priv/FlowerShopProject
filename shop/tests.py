from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Flower, Order, OrderItem
from .forms import RegisterForm, OrderForm
from unittest.mock import patch


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.flower = Flower.objects.create(
            name='Роза',
            price=500.00,
            available=True
        )

    def test_flower_creation(self):
        self.assertEqual(self.flower.__str__(), 'Роза')
        self.assertEqual(self.flower.available, True)

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=1000.00,
            delivery_address='ул. Тестовая, 1'
        )
        OrderItem.objects.create(
            order=order,
            flower=self.flower,
            quantity=2
        )
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order.total_price, 1000.00)


class FormTests(TestCase):
    def test_register_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'user@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_valid(self):
        flower = Flower.objects.create(name='Тюльпан', price=300.00)
        form_data = {
            f'quantity_{flower.id}': 3,
            'delivery_address': 'ул. Примерная, 5',
            'delivery_datetime': '2024-01-01 12:00'
        }
        form = OrderForm(flowers=[flower], data=form_data)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.flower = Flower.objects.create(
            name='Гвоздика',
            price=200.00,
            available=True
        )

    def test_catalog_view(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 302)  # Редирект для неавторизованных

    def test_order_creation_flow(self):
        # Авторизация
        self.client.login(username='testuser', password='testpass123')

        # Создание заказа
        response = self.client.post(reverse('create_order'), {
            f'quantity_{self.flower.id}': 2,
            'delivery_address': 'ул. Тестовая, 1',
            'delivery_datetime': '2024-01-01 12:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

    @patch('shop.views.send_order_confirmation')
    def test_order_confirmation(self, mock_send):
        order = Order.objects.create(
            user=self.user,
            total_price=400.00,
            delivery_address='ул. Тестовая, 1'
        )
        OrderItem.objects.create(
            order=order,
            flower=self.flower,
            quantity=2
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('confirm_order', args=[order.id])
        )
        mock_send.assert_called_once_with(order)
        self.assertEqual(response.status_code, 302)


class AuthTests(TestCase):
    def test_registration_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@user.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_login_view(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)


from django.test import TestCase

# Create your tests here.

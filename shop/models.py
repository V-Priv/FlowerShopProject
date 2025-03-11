from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Flower(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='catalog/', verbose_name="Изображение")
    available = models.BooleanField(default=True, verbose_name="Доступен")

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    flowers = models.ManyToManyField(Flower, through='OrderItem', verbose_name="Цветы")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, default='В работе', verbose_name="Статус")
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    delivery_datetime = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время доставки")  # Объединенное поле
    comments = models.TextField(null=True, blank=True, verbose_name="Комментарии")

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name="Цветок")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"


from django.db import models

# Create your models here.

# Generated by Django 5.1.4 on 2025-02-16 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_order_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_time',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время доставки'),
        ),
    ]

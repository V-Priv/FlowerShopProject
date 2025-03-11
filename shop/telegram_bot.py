import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_order_confirmation(order):
    try:
        # Формирование сообщения
        message = f"✅ Новый заказ подтвержден!\n\n"
        message += f"🆔 Номер заказа: #{order.id}\n"
        message += f"👤 Клиент: {order.user.username}\n"
        message += f"📅 Дата доставки: {order.delivery_datetime.strftime('%d.%m.%Y %H:%M')}\n"
        message += f"🏠 Адрес: {order.delivery_address}\n"
        message += f"💸 Сумма: {order.total_price} руб.\n\n"
        message += "🌸 Состав заказа:\n"

        # Добавляем товары
        for item in order.orderitem_set.all():
            message += f"➖ {item.flower.name} ({item.quantity} шт.)\n"

        # Отправка сообщения
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': message
        }
        response = requests.post(url, data=payload)

        if response.status_code != 200:
            logger.error(f"Ошибка отправки: {response.text}")

    except Exception as e:
        logger.error(f"Ошибка в send_order_confirmation: {str(e)}")

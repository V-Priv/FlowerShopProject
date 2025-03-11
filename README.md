# FlowerShop - Интернет-магазин цветов с Telegram-интеграцией

Учебный проект на Django, реализующий базовый функционал интернет-магазина цветов с интеграцией Telegram-бота для уведомлений.

## 🌟 Особенности

- Регистрация и авторизация пользователей
- Каталог доступных цветов с изображениями
- Система оформления заказов
- Подтверждение заказов с отправкой уведомлений в Telegram
- Панель управления заказами
- Модели данных:
  - Пользователи
  - Цветы/букеты
  - Заказы с детализацией позиций

## 🛠 Технологии

- Python 3.11+
- Django 4.2
- SQLite (для разработки)
- Python-telegram-bot
- Pillow (для работы с изображениями)
- HTML/CSS (Bootstrap для стилей)

## ⚙️ Установка и запуск

1. Клонируйте репозиторий:
git clone https://github.com/ваш-username/FlowerShop.git
cd FlowerShop

2.Установите зависимости:
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate    # Для Windows
pip install -r requirements.txt

3.Настройте базу данных:
python manage.py migrate
python manage.py createsuperuser

4.Запустите сервер:
python manage.py runserver

🔧 Настройка Telegram-бота

Создайте бота через @BotFather
Получите токен бота
Узнайте ваш chat_id через:
curl https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates

Добавьте в settings.py:
TELEGRAM_BOT_TOKEN = 'ваш_токен'
TELEGRAM_CHAT_ID = 'ваш_chat_id'

🗂 Структура проекта
Copy
flower_shop/
├── shop/              # Основное приложение
│   ├── migrations/
│   ├── templates/     # HTML-шаблоны
│   ├── models.py      # Модели данных
│   ├── views.py       # Логика представлений
│   ├── forms.py       # Формы для заказов и регистрации
│   └── telegram_bot.py # Логика Telegram-бота
├── media/             # Загружаемые изображения
├── static/            # Статические файлы
└── flower_shop/       # Настройки проекта

🖥 Примеры использования

Регистрация пользователя
http://localhost:8000/register/

Просмотр каталога
http://localhost:8000/catalog/

Оформление заказа
http://localhost:8000/order/

Подтверждение заказа
http://localhost:8000/order/1/confirm/

📦 Зависимости
См. полный список в requirements.txt

📄 Лицензия
MIT License

📬 Контакты
Владимир - @v-priv - vpriv10@gmail.com

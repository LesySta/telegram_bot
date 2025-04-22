import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 1. Ключи API Telegram
telegram_token = "7459227938:AAFRimwckL_GeLHnzRKKYfg8x4E9PPhRO6M"  # Токен бота
telegram_chat_id = "YOUR_TELEGRAM_CHAT_ID"  # ID чата

# 2. Настройка бота Telegram
bot = Bot(token=telegram_token)
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

# 3. Функция для парсинга страницы ВБ
def parse_wb_page(url):
    """Парсит страницу ВБ и ищет товары с кешбеком."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-card')
    found_products = []
    for product in products:
        title = product.find('div', class_='product-card__title').text.strip()
        if "Кешбек бонусами на карту ВБ" in title:
            price = product.find('span', class_='price').text.strip()
            link = product.find('a', class_='product-card__image')['href']
            found_products.append(f"Название: {title}nЦена: {price}nСсылка: {link}")
    return found_products

# 4. Обработчик команды /start
def start(update, context):
    """Обрабатывает команду /start."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для поиска товаров с кешбеком на ВБ. Отправьте мне ссылку на страницу ВБ.")

# 5. Обработчик сообщений
def handle_message(update, context):
    """Обрабатывает сообщения пользователя."""
    text = update.message.text
    if "https://www.wildberries.ru/" in text:
        products = parse_wb_page(text)
        if products:
            for product in products:
                context.bot.send_message(chat_id=update.effective_chat.id, text=product)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Товаров с кешбеком не найдено.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Введите ссылку на страницу ВБ.")

# 6. Регистрация обработчиков
dispatcher.add_handler(CommandHandler("start", start))  # Добавляем обработчик команды /start
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# 7. Запуск бота
updater.start_polling()
updater.idle()

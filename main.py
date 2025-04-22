import requests, json, telebot
import os

def get_cat_image_url():
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        return response.json()[0]['url']
    except:
        return "Ошибка получения изображения"


def get_dog_image_url():
    try:
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        return response.json()[0]['url']
    except:
        return "Ошибка получения изображения"

token = '7138035220:AAERdvHBpwyH6REFJExe_plEUl1XA-0RX2Q' # Ваш токен
bot = telebot.TeleBot(token)

# Инлайн-клавиатура (для кнопок под фото)
keyboard_inline = telebot.types.InlineKeyboardMarkup()
keyboard_inline.row(telebot.types.InlineKeyboardButton("Еще котиков!", callback_data="cat"),
                    telebot.types.InlineKeyboardButton("Еще собачек!", callback_data="dog"))

# Клавиатура с кнопкой "Список команд"
keyword = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyword.row('Больше котиков!', 'Больше собачек!', 'Список команд')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет!", reply_markup=keyword)


@bot.message_handler(commands=['hi'])
def hi(message):
    bot.send_message(message.chat.id,
                     """Анекдот: Шёл штирлиц по лесу, вдруг ему на плечо упала гусинеца.
                      Где-то взорвался танк! Догадался Штирлиц""",
                     reply_markup=keyword)


@bot.message_handler(commands=['thenks'])
def thenks(message):
    bot.send_message(message.chat.id, "Спасибо, что используете бот!", reply_markup=keyword)


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """Доступные команды:\n
    /start - Начать\n
    /hi - Рассказать анекдот\n
    /thenks - Выразить благодарность\n
    /help - Вывести справку"""
    bot.send_message(message.chat.id, help_text)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "cat":
        image_url = get_cat_image_url()
        bot.send_photo(call.message.chat.id, photo=image_url, reply_markup=keyboard_inline)
    elif call.data == "dog":
        image_url = get_dog_image_url()
        bot.send_photo(call.message.chat.id, photo=image_url, reply_markup=keyboard_inline)


bot.polling(non_stop=True)


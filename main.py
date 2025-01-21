import requests, json, telebot
import os

def get_cat_image_url():
  try:
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    return response.json()[0]['url']
  except:
    return "Ошибка получения изображения"

token ='7138035220:AAERdvHBpwyH6REFJExe_plEUl1XA-0RX2Q'
bot = telebot.TeleBot(token)

keyword = telebot.types.ReplyKeyboardMarkup(True)
keyword.row('Больше котиков')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
        "Привет",
        reply_markup=keyword)

@bot.message_handler(func=lambda message: True)
def send_cat_image(message):
  image_url = get_cat_image_url()
  bot.send_photo(message.chat.id,
                     photo=image_url,
                     reply_markup=keyword)

bot.polling(non_stop=True, interval=0)


bot.polling(non_stop=True, interval=0)

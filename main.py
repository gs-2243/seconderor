from config import TOKEN
import telebot
import requests
import json
from extensions import APIException

keys = {
    "доллар": "USD",
    "Рубль": "RUB",
    "Евро": "EURO",
}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def echo(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту  в следующем фомате:<имя валюты>\n <в какую валюту " \
           "перевести> \n" \
           "《Колличество переводимой валюты》"

    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
        bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(" ")
    r = requests.get(f"https://api.exchangeratesapi.io/latest?symbols={keys[quote]},{keys[base]}")
    text = json.loads(r.content)[keys[base]]
    bot.send_message(message.chat.id, text)


bot.polling()

import telebot
from config import *
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Приветствую. \
\nЯ помогу тебе перевести одну валюту в другую.=) \
\nГлавное задай правильный запрос. Пример ниже.=) \
\nПример: доллар рубль 100\nНачать работу бота: /start \
\nИнструкция для работы с ботом: /help\nСписок всех валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Все валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    global quote, base, amount
    try:
        quote, base, amount = message.text.split()
    except ValueError:
        bot.reply_to(message, 'Неверное количество параметров')

    try:
        conclusion = Converter.get_price(quote, base, amount)
        bot.reply_to(message, f"Цена {amount} {quote} в {base} : {conclusion}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")


bot.polling()
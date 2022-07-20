import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}
TOKEN = "5499133128:AAHl6yLRqghxSl2DW0W-GgiPokbRhP-MIdE"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '<Доброго дня суток!> \ Чтобы начать работу введите команду боту в следующей форме: \n<имя валюты> \
<в какую валюту перевести> \
<количиство переводимой валюты> \n Увидить список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        base, sym, amount = message.text.split()
    except ValueErroras as e:
        bot.reply_to('Неверное количество параметров! Обратитеcь к функции <start>.')
    try:
        new_price = Convertor.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except APIException as e:
        bot.reply_to(f"Ощибка в команде: \n{е}")


bot.polling()

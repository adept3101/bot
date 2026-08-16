import telebot
from telebot import types
import re
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

BOT_NAME = 'calc'

PI = 3.1415926535897932384626433832795

def log(message):
    log = open("log.txt", "w")
    log.write(message.chat.first_name + "(" + message.chat.username + ")" +":" + message.text + "\n")
    log.close()

def msg(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    user_message = message.text.lower()

    if BOT_NAME:
        regex = re.compile(BOT_NAME.lower())
        print(regex.search(user_message))
        if regex.search(user_message) == None:
            return

        regex = re.compile('%s[^a-z]'%(BOT_NAME.lower()))
        user_message = regex.sub("", user_message)

    user_message = user_message.lstrip()
    user_message = user_message.rstrip()
    
    print(user_message)

    if (msg):
        print('Бот: %s'%msg.text)


bot = telebot.TeleBot(str(TOKEN))

nav = types.ReplyKeyboardMarkup(resize_keyboard=True)
test = types.KeyboardButton("test")

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.from_user.id, "/calc /pi")

@bot.message_handler(commands=['calc'])
def send_welcome(message):
    text = "Введите выражение и я попробую его вычислить"
    bot.send_message(message.from_user.id, text)

# @bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['calc'])
def calc(message):
    try:
        result = eval(message.text)
        bot.send_message(message.from_user.id, f'Результат {result}')

    except Exception as e:
        bot.send_message(message.from_user.id, 'Ошибка в вычислении')
        print(e)

    log(message)
    msg(message)

bot.polling(none_stop=True, interval=0)

@bot.message_handler(commands=['pi'])
def guess_pi(message):
    try:
        num = eval(message.text)
        if PI % num == 0:
            bot.send_message(message.from_user.id, 'Феноменально! Ты знаешь 31 значение числа пи.')
        elif PI % num > 0 and PI % num < 0.0015926535897929917:
            bot.send_message(message.from_user.id, 'Молодец ты знаешь число пи.')
        else:
            bot.send_message(message.from_user.id, 'Это никуда не годится учи математику.')
    
    except Exception as e:
        bot.send_message(message.from_user.id, 'Ошибка в вводе')
        print(e)

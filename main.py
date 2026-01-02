import telebot, time, math, re
import os
from dotenv import load_dotenv
from log import log, msg

load_dotenv()
TOKEN = os.getenv("TOKEN")

BOT_NAME = 'calc'

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


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Введите выражение и я попробую его вычислить"
    bot.send_message(message.from_user.id, text)

@bot.message_handler(func=lambda message: True)
def calc(message):
    try:
        result = eval(message.text)
        bot.send_message(message.from_user.id, f'Результат {result}')

    except Exception as e:
        bot.send_message(message.from_user.id, 'Ошибка в вычислении')

    log(message)
    msg(message)

bot.polling(none_stop=True, interval=0)

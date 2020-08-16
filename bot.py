import telebot
from telebot import types
import config
import sqlite3
import random
from time import gmtime


bot = telebot.TeleBot(config.token)
quote = "Нажми еще раз"


def get_quote():
    global quote
    db = sqlite3.connect("quotes.db")
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS quotes ( 
        login TEXT,
        quote TEXT
    )""")
    db.commit()

    size = 0
    for i in sql.execute("SELECT * FROM quotes"):
        size += 1
    numb = random.randint(0, size)
    count = 0
    for val in sql.execute("SELECT * FROM quotes"):
        if count == numb:
            quote = val[1]
            break
        count += 1
    return quote


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Цитата")
    markup.add(item)
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}.\
 Меня зовут Messy. Я ваш бот-цитатник. Буду отправлять вам время от времени различные цитаты, чтобы было веселей)", \
                     reply_markup=markup)
    check = True
    while True:
        if gmtime()[3] == 19 and gmtime()[4] == 30 and gmtime()[5] == 0 and check:
            bot.send_message(message.chat.id, "Доброго вечера)")
            fast_quote(message, "Цитата")
            check = False
        elif gmtime()[3] == 7 and gmtime()[4] == 0 and gmtime()[5] == 0 and check:
            bot.send_message(message.chat.id, "Доброго утра)")
            fast_quote(message, "Цитата")
            check = False
        elif gmtime()[3] == 12 and gmtime()[4] == 0 and gmtime()[5] == 0 and check:
            bot.send_message(message.chat.id, "Доброго дня)")
            fast_quote(message, "Цитата")
            check = False
        if gmtime()[5] == 10:
            check = True
        


@bot.message_handler(content_types=['text'])
def fast_quote(message, other=""):
    if message.text == 'Цитата' or other == "Цитата":
        bot.send_message(message.chat.id, "Вот, держите)")
        bot.send_message(message.chat.id, f'"{get_quote()}"')

"""
def send_question(message):
    markup = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    markup.add(item_yes)
    bot.send_message(message.chat.id, "Хотите получить еще цитату?", reply_markup=markup)"""


"""@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "yes":
        fast_quote(message)"""


while __name__ == "__main__":
    bot.polling(none_stop=True)


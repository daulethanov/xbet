import random
import string

from config import db
import telebot
from telebot import types
import logging
from app import app
from services.client.model import User
from services.mail import send_notification_email
from services.bet.model import Math


token = '6122784461:AAE-0SRUmwvDVUydhUsmSUWW0qg7deTFLVM'
bot = telebot.TeleBot(token=token)

logging.basicConfig(level=logging.DEBUG)


@bot.message_handler(content_types=['text'])
def view_math(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    with app.app_context():
        math = Math.query.all()
        if math:
            for mat in math:
                button = types.KeyboardButton(mat.name)
                markup.add(button)

            bot.send_message(message.chat.id, text='Выберите матч:', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text='Нет доступных матчей.')


@bot.message_handler(commands=['start', 'help'], content_types=['text'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Регистрация")
    btn2 = types.KeyboardButton("Войти")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Вас приветствует BetBot 👾', reply_markup=markup)


def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Регистрация")
    btn2 = telebot.types.KeyboardButton("Войти")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Вас приветствует BetBot 👾', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def tg_register_user(message):
    if message.text == 'Регистрация':
        bot.send_message(message.chat.id, text='Введите свой Email:')
        bot.register_next_step_handler(message, process_registration)
    elif message.text == 'Войти':
        bot.register_next_step_handler(message, process_login)


def process_registration(message):
    email = message.text.strip()
    if email:
        random_password = ''.join(random.choices(string.ascii_lowercase, k=8))
        code = str(random.randint(10000000, 99999999))
        pwd = User.password_hash(password=random_password)

        with app.app_context():
            user = User(email=email, password=pwd, token=code, tg_token=message.chat.id)
            db.session.add(user)
            db.session.commit()
            send_notification_email(user.email, random_password, code)
            bot.send_message(message.chat.id, text='Регистрация прошла успешно!')
    else:
        bot.send_message(message.chat.id, text='Неверный email.')


def process_login(message):
    if message.text == 'Все команды':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("Просмотреть список матчей 🔔")
        markup.add(btn1)
        bot.send_message(message.chat.id, text='Вы вошли в систему', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text='Пользователь не найден')


@bot.message_handler(content_types=['text'])
def button_in_login(message):
    if message.text == "Просмотреть список матчей 🔔":
        bot.register_next_step_handler(message, view_math)
    elif message.text == 'Все команды':
        bot.register_next_step_handler(message, process_login)




if __name__ == '__main__':
    bot.polling()

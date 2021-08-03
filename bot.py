import time
import schedule

import requests
import telebot

import config

from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot(config.token)
# keyboard
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Запросить ссылки!')

keyboard.add(item1)


def send(id, text):
    bot.send_message(id, text, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Приветствуем Вас, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный "
                                      "чтобы облегчить Вам работу.".format(message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def handle(message):
    url = "https://krisha.kz/arenda/kvartiry/almaty/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.77 Safari/537.36 "
    }

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    acard__title = soup.find_all("a", class_="a-card__title")

    for acard in acard__title:
        acard__url = f'https://krisha.kz{acard.get("href")}'

        # Вывод сообщения для бота
        bot.send_message(message.chat.id, f" {acard__url}")

    schedule.every(10).seconds.do(bot)

    while True:
        schedule.run_pending()
        time.sleep(1)


# RUN
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

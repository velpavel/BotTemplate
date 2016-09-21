# -*- coding: utf-8 -*-
import telebot
import configparser
import datetime, time


config = configparser.ConfigParser()
config.read('config.ini')

bot = telebot.TeleBot(config['BASE']['Token'])

if __name__ == '__main__':
    while True:
        try:
            bot.send_message(config['BASE']['Admin_id'], "Started")
            print("Bot production started")
            bot.polling(none_stop=True)
            break
        except Exception as e:
            print("{} Error: {} : {}".format(datetime.datetime.now().strftime('%x %X'), e.__class__, e))
            print("Restarted after 20 sec")
            time.sleep(20)
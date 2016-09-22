# -*- coding: utf-8 -*-
import telebot
import configparser
import datetime, time
from telebot import types

config_file = r'config.ini'
opRegister = 'register'

import db_connector
from registration import register_flow

config = configparser.ConfigParser()
config.read(config_file)

bot = telebot.TeleBot(config['BASE']['Token'])
admin_id = config['BASE']['Admin_id']

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    global admin_id
    help_str='''Help_str'''
    if not admin_id:
        admin_id = str(message.from_user.id)
        config['BASE']['Admin_id'] = admin_id
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    bot.send_message(message.chat.id, help_str)
    if not (db_connector.is_user_registered(message.from_user.id)):
        handle_register(message)

@bot.message_handler(func=lambda message: not db_connector.is_user_registered(message.from_user.id), content_types=['text','contact'])
def handle_register(message):
    register_flow(bot, message)

if __name__ == '__main__':
    while True:
        try:
            if admin_id: bot.send_message(admin_id, "Started")
            print("Bot started")
            bot.polling(none_stop=True)
            break
        except Exception as e:
            print("{} Error: {} : {}".format(datetime.datetime.now().strftime('%x %X'), e.__class__, e))
            print("Restarted after 20 sec")
            time.sleep(20)
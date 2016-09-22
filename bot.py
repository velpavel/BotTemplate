# -*- coding: utf-8 -*-
import telebot
import configparser
import datetime, time
from telebot import types

import db_connector
from registration import register_flow
import admin_functions


#import logging
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

config_file = r'config.ini'
opRegister = 'register'

config = configparser.ConfigParser()
config.read(config_file)

bot = telebot.TeleBot(config['BASE']['Token'])
admin_id = int(config['BASE']['Admin_id'])

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    global admin_id
    db_connector.save_to_log('user', message)
    help_str='''Help_str'''
    if not admin_id:
        admin_id = str(message.from_user.id)
        config['BASE']['Admin_id'] = admin_id
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    bot.send_message(message.chat.id, help_str)
    if not (db_connector.is_user_registered(message.from_user.id)):
        register_flow(bot, message)

@bot.message_handler(func=lambda message: not db_connector.is_user_registered(message.from_user.id), content_types=['text','contact'])
def handle_register(message):
    db_connector.save_to_log('user', message)
    register_flow(bot, message)

@bot.message_handler(commands=admin_functions.admin_commands)
def handle_admin_com(message):
    db_connector.save_to_log('user', message)
    admin_functions.admin_flow(bot, message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def msg(message):
    db_connector.save_to_log('user', message)
    bot.send_message(message.chat.id, 'Рад с тобой пообщаться.', reply_markup=types.ReplyKeyboardHide())

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
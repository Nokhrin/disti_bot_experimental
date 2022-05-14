import sys
sys.path.insert(0, 'common')
import consts
import messages_templates

import logging

logging.basicConfig(filename=consts.log_path,
                    filemode=consts.log_filemode,
                    encoding=consts.log_encoding,
                    format=consts.log_format,
                    level=consts.log_level)

import telebot
from telebot import types

import calculators

logging.info('importing check has been passed')


#==============================
# main function
if __name__ == "__main__":

    bot = telebot.TeleBot(consts.API_KEY, parse_mode=None)

    #=======================#
    ### commands handlers ###
    #=======================#
    # markup for hiding buttons
    markup_hide_buttons = types.ReplyKeyboardRemove(selective=False)

    @bot.message_handler(commands=['start'])
    def welcoming(message):
        bot.send_message(message.chat.id, messages_templates.start_message)

    @bot.message_handler(commands=['help'])
    def help_response(message):
        # commands description
        bot.send_message(message.chat.id, messages_templates.commands_description)
        # ==================

    #===============================
    # show buttons for recipes
    @bot.message_handler(commands=['recipes'])
    def recipes_list(message):
        # buttons for recipes
        recipe_01 = types.KeyboardButton('Инвертный сироп')
        recipe_02 = types.KeyboardButton('Сахарное сусло')
        # ==================
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup.row(recipe_01, recipe_02)
        bot.send_message(message.chat.id, messages_templates.recipe_message, reply_markup=markup)
    #===============================

    @bot.message_handler(commands=['calculators'])
    def calculators_list(message):
        # buttons for calculators
        calculator_01 = types.KeyboardButton('Расчёт голов и тела')
        calculator_02 = types.KeyboardButton('Конвертация температуры')
        # ==================
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(calculator_01, calculator_02)
        bot.send_message(message.chat.id, messages_templates.calculator_message, reply_markup=markup)


    # respond on buttons
    @bot.message_handler(func=lambda message: True)
    def reply_with_recipe(message):
        if message.text.lower() in ['инверт', 'инвертный сироп']:
            bot.reply_to(message, 'вот рецепт')

            # sending recipe
            recipe_as_doc = open('recipes/inverted_sugar.txt', 'rb')
            #bot.send_document(message.chat.id, recipe_as_doc) # send as document
            # send as text
            recipe_as_text = recipe_as_doc.read()
            bot.send_message(message.chat.id, recipe_as_text, reply_markup=markup_hide_buttons)
            recipe_as_doc.close()

        elif message.text.lower() in ['сахарное сусло', 'сахарная брага']:
            bot.reply_to(message, 'вот рецепт')

            # sending recipe
            recipe_as_doc = open('recipes/sugar_wash.txt', 'rb')
            #bot.send_document(message.chat.id, recipe_as_doc) # send as document
            # send as text
            recipe_as_text = recipe_as_doc.read()
            bot.send_message(message.chat.id, recipe_as_text, reply_markup=markup_hide_buttons)
            recipe_as_doc.close()

        elif message.text.lower() in ['расчёт голов и тела']:
            # calling heads and heart calculator
            calc_response = calculators.heads_and_heart_calculator()
            bot.send_message(message.chat.id, calc_response, reply_markup=markup_hide_buttons)

        elif message.text.lower() in ['конвертация температуры']:
            ## testing variables
            degrees_1 = 212
            units_1 = 'F'

            # # selecting units
            # units_f_to_c = types.KeyboardButton('F -> C')
            # units_c_to_f = types.KeyboardButton('C -> F')
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # markup.add(units_f_to_c, units_c_to_f)
            # bot.send_message(message.chat.id, 'Выберите конвертацию', reply_markup=markup)
            #
            # if message.text == 'F -> C':
            #     units = 'f'
            # elif message.text == 'C -> F':
            #     units = 'c'


            # calling temperature converter
            calc_response = calculators.temperature_converter(degrees_1, units_1)
            bot.send_message(message.chat.id, calc_response, reply_markup=markup_hide_buttons)

        else:
            bot.reply_to(message, messages_templates.dont_understand, reply_markup=markup_hide_buttons)
            # bot.reply_to(message, message.text, reply_markup=markup_hide_buttons) # simple echo to message





    # testing bot with simple echoing message object
    # @bot.message_handler(func=lambda message: True)
    # def echo_all(message):
    #     bot.reply_to(message, message.text)



    # starting the bot
    bot.infinity_polling()
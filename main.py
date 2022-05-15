# global dependencies
import sys
sys.path.insert(0, 'common')
import logging
import json
import telebot
from telebot import types

# my dependencies
import consts
import calculators
import messages_templates

logging.basicConfig(filename=consts.log_path,
                    filemode=consts.log_filemode,
                    encoding=consts.log_encoding,
                    format=consts.log_format,
                    level=consts.log_level)

logging.info('importing check has been passed')


# getting API token
with open("common/conf.json") as conf:
    token = json.load(conf)

#==============================
# main function
if __name__ == "__main__":

    bot = telebot.TeleBot(token['telegram_token'], parse_mode=None)

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
        calculator_03 = types.KeyboardButton('Простой калькулятор')
        # ==================
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(calculator_01, calculator_02, calculator_03)
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

        elif message.text.lower() in ['простой калькулятор']:
            str_message = f'Добро пожаловать в простой калькулятор!\nВведите первое число\n'
            bot_message = bot.send_message(message.chat.id, str_message)
            bot.register_next_step_handler(bot_message, get_number_1)
            # simple math calculator
            #
            # 1. variables: first number, operator, second number, result
            # 2. calculation
            # 3. continue calculation?
            #  if yes, return previous result as first number
            #  if no, return result
            user_number_1 = ''
            user_number_2 = ''
            user_operator = ''
            calc_result = None



            calc_response = calculators.simple_math_calculator(user_number_1, user_operator, user_number_2)
            bot.send_message(message.chat.id, calc_response, reply_markup=markup_hide_buttons)

        else:
            bot.reply_to(message, messages_templates.dont_understand, reply_markup=markup_hide_buttons)
            # bot.reply_to(message, message.text, reply_markup=markup_hide_buttons) # simple echo to message


    def get_number_1(message, result = None):
        try:
            global user_number_1
            # for the first run
            if user_number_1 == None:
                user_number_1 = int(user_number_1)
            # for next runs
            else:
                user_number_1 = result

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            key_1 = types.KeyboardButton('+')
            key_2 = types.KeyboardButton('-')
            key_3 = types.KeyboardButton('*')
            key_4 = types.KeyboardButton('/')

            markup.add(key_1, key_2, key_3, key_4)

            bot_message = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
            bot.register_next_step_handler(bot_message, get_operator

        except Exception:
            bot.reply_to("Что-то пошло не так")


    def get_operator(message):
        try:
            global user_operator

            user_operator = message.text

            # hide the keyboard
            markup = types.ReplyKeyboardRemove(selective=False)

            bot_message = bot.send_message(message.chat.id, "Ввведите следующее число", reply_markup=markup)
            bot.register_next_step_handler(bot_message, get_number_2)

        except Exception:
            bot.reply_to("Что-то пошло не так")


    def get_number_2(message):
        try:
            global user_number_2
            user_number_2 = int(message.text)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            key_1 = types.KeyboardButton('Завершить вычисление')
            key_2 = types.KeyboardButton('Продолжить вычисление')
            markup.add(key_1, key_2)

            bot_message = bot.send_message(message.chat.id, "Завершаем или продолжаем?", reply_markup=markup)
            bot.register_next_step_handler(bot_message, stop_or_continue)

        except Exception:
            bot.reply_to("Что-то пошло не так")


    def stop_or_continue():
        try:
            user_result = calculators.simple_math_calculator(user_operator, user_number_1, user_number_2)

            # hide the keyboard
            markup = types.ReplyKeyboardRemove(selective=False)

            if message.text.lower() in ['завершить вычисление']:
                bot.send_message(message.chat.id, user_result, reply_markup=markup)
            elif message.text.lower() in ['продолжить вычисление']:
                get_number_1(message, user_result)

        except Exception:
            bot.reply_to("Что-то пошло не так")


    # testing bot with simple echoing message object
    # @bot.message_handler(func=lambda message: True)
    # def echo_all(message):
    #     bot.reply_to(message, message.text)



    # starting the bot
    bot.infinity_polling()

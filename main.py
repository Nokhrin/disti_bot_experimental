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
    markup_hide_keys = types.ReplyKeyboardRemove(selective=False)

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
            bot.send_message(message.chat.id, recipe_as_text, reply_markup=markup_hide_keys)
            recipe_as_doc.close()

        elif message.text.lower() in ['сахарное сусло', 'сахарная брага']:
            bot.reply_to(message, 'вот рецепт')

            # sending recipe
            recipe_as_doc = open('recipes/sugar_wash.txt', 'rb')
            #bot.send_document(message.chat.id, recipe_as_doc) # send as document
            # send as text
            recipe_as_text = recipe_as_doc.read()
            bot.send_message(message.chat.id, recipe_as_text, reply_markup=markup_hide_keys)
            recipe_as_doc.close()

        elif message.text.lower() in ['расчёт голов и тела']:
            # calling heads and heart calculator
            calc_response = calculators.heads_and_heart_calculator()
            bot.send_message(message.chat.id, calc_response, reply_markup=markup_hide_keys)

        elif message.text.lower() in ['конвертация температуры']:
            # initiate temperature converter dialog
            degrees = 0
            units = ''

            # hide keyboard
            markup_hide_keys = types.ReplyKeyboardRemove(selective=False)

            # ask for temperature
            str_message = f'Добро пожаловать в конвертер температуры\nВведите температуру\n'
            bot_message = bot.send_message(message.chat.id, str_message, reply_markup=markup_hide_keys)
            bot.register_next_step_handler(bot_message, get_temperature)




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
            #
            #
            #
            # calc_response = calculators.get_number_1(user_number_1, user_operator, user_number_2)
            # bot.send_message(message.chat.id, calc_response, reply_markup=markup_hide_keys)

        else:
            bot.reply_to(message, messages_templates.dont_understand, reply_markup=markup_hide_keys)
            # bot.reply_to(message, message.text, reply_markup=markup_hide_keys) # simple echo to message


#=========temperature converter=====================
    def get_temperature(message):
        logging.debug('stepped into get_temperature')

        global degrees
        degrees = int(message.text)

        logging.debug(f'degrees = {degrees}')
        # keys for conversion
        units_f_to_c = types.KeyboardButton('F -> C')
        units_c_to_f = types.KeyboardButton('C -> F')
        markup_convertion_keys = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_convertion_keys.add(units_f_to_c, units_c_to_f)

        str_message = f'Как конвертируем?'
        bot_message = bot.send_message(message.chat.id, str_message, reply_markup=markup_convertion_keys)
        bot.register_next_step_handler(bot_message, get_convert_type)



    def get_convert_type(message):
        logging.debug('stepped into get_convert_type')

        global degrees
        global units

        logging.debug(f'degrees = {degrees}')
        logging.debug(f'message.text = {message.text}')
        if message.text == 'F -> C':
            units = 'f'
        elif message.text == 'C -> F':
            units = 'c'

        logging.debug(f'units = {units}')
        # hide buttons
        markup_hide_keys = types.ReplyKeyboardRemove(selective=False)

        # call temperature converter
        calc_response = calculators.temperature_converter(degrees, units)
        bot.send_message(message.chat.id, calc_response, reply_markup=markup_hide_keys)

#====================================================

#======simple calculator=============================
    def get_number_1(message, result = None):
        logging.info('started get_number_1')
        #try:

        # check if user input is a number
        try:
            int(message.text)
            logging.debug(f'input {message.text} is a number, continue')
        except:
            logging.debug(f'input {message.text} is not a number, ask again')
            bot_message = bot.send_message(message.chat.id, f'{message.text} - не число, введите число')
            bot.register_next_step_handler(bot_message, get_number_1)
            return None

        global user_number_1
        # for the first run
        if result == None:
            user_number_1 = int(message.text)

        # for next runs
        else:
            user_number_1 = result

        logging.debug(f'user_number_1 = {user_number_1}')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        key_1 = types.KeyboardButton('+')
        key_2 = types.KeyboardButton('-')
        key_3 = types.KeyboardButton('*')
        key_4 = types.KeyboardButton('/')

        markup.add(key_1, key_2, key_3, key_4)

        bot_message = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
        bot.register_next_step_handler(bot_message, get_operator)

        # except Exception:
        #     bot.reply_to(message, "Что-то пошло не так")


    def get_operator(message):
        logging.info('started get_operator')
        supported_operators = ['+', '-', '*', '/']
        # try:
        global user_number_1
        global user_operator

        user_operator = message.text
        logging.debug(f'user_operator = {user_operator}')

        # check the operator input
        if user_operator not in supported_operators:
            logging.debug('operator is incorrect, enter the operator')
            markup = types.ReplyKeyboardRemove(selective=False)
            bot_message = bot.send_message(message.chat.id, "Операция выбрана некорректно, выберите операцию", reply_markup=markup)
            bot.register_next_step_handler(bot_message, get_number_1(message, user_number_1))
        # if operator is correct
        else:
            # hide the keyboard
            markup = types.ReplyKeyboardRemove(selective=False)

            bot_message = bot.send_message(message.chat.id, "Введите следующее число", reply_markup=markup)
            bot.register_next_step_handler(bot_message, get_number_2)

        # except Exception:
        #     bot.reply_to(message, "Что-то пошло не так")


    def get_number_2(message):
        logging.info('started get_number_2')

        # check if user input is a number
        try:
            int(message.text)
            logging.debug(f'input {message.text} is a number, continue')
        except:
            logging.debug(f'input {message.text} is not a number, ask again')
            bot_message = bot.send_message(message.chat.id, f'{message.text} - не число, введите число')
            bot.register_next_step_handler(bot_message, get_number_2)
            #return None
            raise

        # try:
        global user_number_2
        user_number_2 = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        key_1 = types.KeyboardButton('Завершить вычисление')
        key_2 = types.KeyboardButton('Продолжить вычисление')
        markup.add(key_1, key_2)

        calc_result = calculators.simple_math_calculator(user_operator, user_number_1, user_number_2)
        bot.send_message(message.chat.id, f'результат = {calc_result}')

        bot_message = bot.send_message(message.chat.id, "Завершаем или продолжаем?", reply_markup=markup)
        bot.register_next_step_handler(bot_message, stop_or_continue)

        # except Exception:
        #     bot.reply_to(message, "Что-то пошло не так")


    def stop_or_continue(message):
        logging.debug('started stop_or_continue')
        logging.debug(f'function input => {message.text}')
        #try:
        global user_operator
        global user_number_1
        global user_number_2
        global calc_result

        logging.debug(f'user_operator = {user_operator}, user_number_1 = {user_number_1}, user_number_2 = {user_number_2}')

        calc_result = calculators.simple_math_calculator(user_operator, user_number_1, user_number_2)
        logging.debug(f'called calculator function, calc_result = {calc_result}')
        # hide the keyboard
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() in ['завершить вычисление']:
            logging.debug('chose to finish')
            bot.send_message(message.chat.id, f'результат = {calc_result}', reply_markup=markup)
        elif message.text.lower() in ['продолжить вычисление']:
            logging.debug('chose to continue')
            get_number_1(message, calc_result)

        # except Exception:
        #     bot.reply_to(message, "Что-то пошло не так")


    # testing bot with simple echoing message object
    # @bot.message_handler(func=lambda message: True)
    # def echo_all(message):
    #     bot.reply_to(message, message.text)



    # starting the bot
    bot.infinity_polling()

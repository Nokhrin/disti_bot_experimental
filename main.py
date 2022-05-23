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
        #bot.send_message(message.chat.id, messages_templates.start_message)
        logging.info(message)
        str_hello = f'Привет, {message.from_user.username}!\n'
        bot.send_message(message.from_user.id, str_hello)
        bot.send_message(message.from_user.id, messages_templates.start_message)

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
        calculator_04 = types.KeyboardButton('Калькулятор с кнопками')
        # ==================
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(calculator_01, calculator_02, calculator_03, calculator_04)
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

        elif message.text.lower() in ['калькулятор с кнопками','keyboard_calculator','/kc']:
            str_message = f'Добро пожаловать в калькулятор!\nПриятных расчётов!\n'

            # hide keyboard
            markup_hide_keys = types.ReplyKeyboardRemove(selective=False)

            bot.send_message(message.chat.id, str_message, reply_markup=markup_hide_keys)

            global calculator_value, previous_calculator_value, calculator_first_num, calculator_second_num, calculator_operator

            global calculator_memory, mrc_pressed_once

            calculator_value = ''
            previous_calculator_value = ''
            calculator_first_num = ''
            calculator_second_num = ''
            calculator_operator = ''
            calculator_memory = ''
            mrc_pressed_once = False
            # layout taken from Citizen SE-707A
            # create keyboard
            global keyboard_layout
            keyboard_layout = telebot.types.InlineKeyboardMarkup(row_width=4)
            # row of keys 1
            keyboard_layout.row(telebot.types.InlineKeyboardButton('C/CE', callback_data='all_clear'),
                         telebot.types.InlineKeyboardButton(u'\u221A', callback_data='sq_root'),
                         telebot.types.InlineKeyboardButton('%', callback_data='percent'),
                         telebot.types.InlineKeyboardButton('+/-', callback_data='sign_change')
                         )
            # row of keys 2
            keyboard_layout.row(telebot.types.InlineKeyboardButton('MRC', callback_data='mrc'),
                         telebot.types.InlineKeyboardButton('M-', callback_data='m-'),
                         telebot.types.InlineKeyboardButton('M+', callback_data='m+'),
                         telebot.types.InlineKeyboardButton('/', callback_data='/')
                         )
            # row of keys 3
            keyboard_layout.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
                         telebot.types.InlineKeyboardButton('8', callback_data='8'),
                         telebot.types.InlineKeyboardButton('9', callback_data='9'),
                         telebot.types.InlineKeyboardButton('*', callback_data='*')
                         )
            # row of keys 4
            keyboard_layout.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
                         telebot.types.InlineKeyboardButton('5', callback_data='5'),
                         telebot.types.InlineKeyboardButton('6', callback_data='6'),
                         telebot.types.InlineKeyboardButton('-', callback_data='-')
                         )
            # row of keys 5
            keyboard_layout.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
                         telebot.types.InlineKeyboardButton('2', callback_data='2'),
                         telebot.types.InlineKeyboardButton('3', callback_data='3'),
                         telebot.types.InlineKeyboardButton('+', callback_data='+')
                         )
            # row of keys 6
            keyboard_layout.row(telebot.types.InlineKeyboardButton('0', callback_data='0'),
                         telebot.types.InlineKeyboardButton('.', callback_data='.'),
                         telebot.types.InlineKeyboardButton(' ', callback_data='nothing'),
                         telebot.types.InlineKeyboardButton('=', callback_data='=')
                         )


            # send message to user
            if calculator_value == '':
                bot_message = bot.send_message(message.chat.id, '0', reply_markup=keyboard_layout)
            else:
                bot_message = bot.send_message(message.chat.id, calculator_value, reply_markup=keyboard_layout)
            # bot.register_next_step_handler(bot_message, run_button_calculator)

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

#============== keyboard calculator =====================

    # def run_button_calculator(message):
    #     logging.info('stepped into run_button_calculator')

    # event handler for calculator keys
    @bot.callback_query_handler(func=lambda call: True)
    def callback_func(query):
        logging.info('stepped into callback query on calculator')
        #logging.debug(f'query => {query}')

        global calculator_value, previous_calculator_value, calculator_first_num, calculator_second_num, calculator_operator, calculator_memory, mrc_pressed_once


        # process input command
        user_input = query.data
        logging.debug(f'user_input => {user_input}')

        # # remember first number
        # if calculator_value == '' or (calculator_operator == '' and calculator_second_num == '' and user_input not in ['+','-','*','/']):
        #     calculator_value += user_input
        # # remember operator
        # elif calculator_value != '' and user_input in ['+','-','*','/']:
        #     calculator_operator = user_input
        # # remember second number
        # elif calculator_value != '' and calculator_operator != '' and calculator_second_num == '':
        #     calculator_second_num = user_input



        # empty key
        if user_input in ['nothing']:
            return

        elif user_input in ['c', 'c/ce', 'all_clear']:
            # clear command
            # "C" and "CE" functions work differently, but they are combined on my etalon hardware calculator
            # "CE" erases the last number or operation entered
            # "C" stands for “global clear” that clears or deletes the entire calculation (sometimes "AC" - all clear)
                # source:
                # https://www.zencalculator.com/reviews/c-vs-ce-in-calculator/
                # https://www.calculator.org/CalcHelp/basics.html

            calculator_value = ''
            calculator_first_num = ''
            calculator_operator = ''
            calculator_second_num = ''

        elif user_input not in ['=','+','-','*','/','sign_change','sq_root','mrc','m+','m-']:
            # remember first number
            if calculator_first_num == '' or (calculator_operator == '' and calculator_second_num == ''):
                calculator_first_num += user_input
                calculator_value = calculator_first_num

            # remember second number
            # if calculator_first_num != '' and calculator_operator != '' and calculator_second_num == '':
            if calculator_first_num != '' and calculator_operator != '':
                calculator_second_num += user_input
                calculator_value = calculator_first_num + calculator_operator + calculator_second_num

        # remember operator
        elif user_input in ['+','-','*','/']:
            calculator_operator = user_input
            calculator_value += calculator_operator

        else:
            logging.debug(f'\nBEFORE calculation')
            logging.debug(f'\ncalculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
            logging.debug(f'\ncalculator_value = {calculator_value}\nprevious_calculator_value = {previous_calculator_value}\n')


            # changing sign
            if user_input == 'sign_change':
                # change sign of the first number
                logging.debug(f'\n SIGN CHANGE started')

                if calculator_first_num != '' and calculator_operator == '':
                    if type(eval(calculator_first_num)) is int:
                        if int(calculator_first_num) > 0:
                            calculator_first_num = '-' + calculator_first_num
                        elif int(calculator_first_num) < 0:
                            calculator_first_num = calculator_first_num[1:]
                    elif type(eval(calculator_first_num)) is float:
                        if float(calculator_first_num) > 0:
                            calculator_first_num = '-' + calculator_first_num
                        elif float(calculator_first_num) < 0:
                            calculator_first_num = calculator_first_num[1:]

                    calculator_value = calculator_first_num # update expression to calculate
                # change sign of the second number
                elif calculator_second_num != '':
                    if int(calculator_second_num) > 0:
                        calculator_second_num = '(-' + calculator_second_num + ')'
                    elif int(calculator_second_num) < 0:
                        if calculator_second_num[:2] == '(-' and calculator_second_num[-1:] == ')':
                            calculator_second_num = calculator_second_num[2:-1] # remove brackets and minus sign

                    calculator_value = calculator_first_num + calculator_operator + calculator_second_num # update expression to calculate

                logging.debug(f'\ncalculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
                logging.debug(f'\ncalculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
                logging.debug(f'\n SIGN CHANGE finished')

            # percentage
            # https://devblogs.microsoft.com/oldnewthing/20080110-00/?p=23853
            elif user_input == 'percent':
                # operator and two numbers should be provided
                if calculator_first_num != '' and calculator_operator != '' and calculator_second_num != '':
                    # algrorithm: first_num * (1 'user_operator' second_num / 100)
                    global percentage_result
                    # logging.debug(f'PERCENTAGE')
                    # logging.debug(f'calculator_value = {calculator_value}')
                    percentage_result = calculator_first_num + '*(1' + calculator_operator + calculator_second_num + '/100)'
                    # logging.debug(f'percentage_result = {percentage_result}')

                    # show % on screen
                    calculator_value += '%'
                    #calculator_value = str(eval(percentage_result))

            # square root
            elif user_input == 'sq_root':
                # if second num is empty, calculate square root of first num
                # if second num is not empty, calculate square root of operation result between first and second number
                if calculator_second_num == '':
                    sq_root_tmp = calculator_first_num
                else:
                    sq_root_tmp = str(eval(calculator_value) ** (1 / 2))
                calculator_value = str(eval(sq_root_tmp) ** (1 / 2))

                # logging.debug(f'\nSquare root')
                # logging.debug(f'\nsq_root_tmp = {sq_root_tmp}')
                calculator_value = str(eval(calculator_value))
                calculator_first_num = calculator_value
                calculator_operator = ''
                calculator_second_num = ''

            # memory operations
            # https://www.normansoven.com/post/how-to-use-the-memory-functions-of-your-calculator
            # "MRC" stands for “Memory Recall(Read) Clear”.
                # Pressing it recalls(reads) the value stored in its memory, pressing it again clears it. - https://qr.ae/pvC8iT
            # "M+" adds input to the memory
            # "M-" subtracts from the memory
            elif user_input == 'mrc':
                logging.debug(f'MRC pressed\n calculator_memory = {calculator_memory}')
                # logging.debug(f'\ncalculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
                if mrc_pressed_once == False: # if MRC pressed once, it recall the value from memory
                    mrc_pressed_once = True
                    #if calculator_first_num == '': # if we don't to rewrite entered number
                    if calculator_first_num != '' and calculator_operator == '' and calculator_second_num == '': # that means we are working with first number
                        if calculator_memory != '':
                            calculator_first_num = calculator_memory
                        else:
                            calculator_first_num = '0'
                    elif calculator_first_num != '' and calculator_operator != '' and calculator_second_num == '':
                        if calculator_memory != '':
                            calculator_second_num = calculator_memory
                        else:
                            calculator_second_num = '0'
                else: # if MRC pressed twice in a row, it clears the value from memory
                    calculator_memory = ''
                    mrc_pressed_once = False # back to initial unpressed position
                logging.debug(f'MRC pressed - END -- \n calculator_memory = {calculator_memory}')
                # logging.debug(f'first num should be 0 here \n calculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
            elif user_input == 'm+':
                logging.debug(f'M+ pressed')
                logging.debug(f'\ncalculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
                if calculator_first_num != '' and calculator_operator == '' and calculator_second_num == '':
                    num_add_to_memory = calculator_first_num
                calculator_memory = str(eval(calculator_memory + '+' + num_add_to_memory))
                logging.debug(f'calculator_memory = {calculator_memory}')

            elif user_input == 'm-':
                logging.debug(f'M- pressed')

            # stop calculation
            elif user_input == '=':
                if previous_calculator_value[-1:] == '%':
                    calculator_value = percentage_result

                logging.debug(f'\n "=" pressed \ncalculator_value = {calculator_value}\nprevious_calculator_value = {previous_calculator_value}\n')
                # final value expression
                # calculator_value = calculator_first_num + calculator_operator + calculator_second_num
                calculator_value = str(eval(calculator_value))
                # variables for the next call
                calculator_first_num = calculator_value
                calculator_operator = ''
                calculator_second_num = ''

        # final value expression
        # build string for eval() function
        # if calculator_first_num != '' and calculator_operator != '' and calculator_second_num != '':
            # calculator_value = calculator_first_num + calculator_operator + calculator_second_num
            # calculator_value = str(eval(calculator_value))

        if calculator_value != '':
            previous_calculator_value = calculator_value


        logging.debug(f'right after calculation')
        logging.debug(f'\ncalculator_first_num = {calculator_first_num}\n user_operator = {calculator_operator}\n calculator_second_num = {calculator_second_num}\n')
        logging.debug(f'\ncalculator_value = {calculator_value}\nprevious_calculator_value = {previous_calculator_value}\n')


        # check if value changed
        # if it didn't and we'll try to send it as message, the next error will raise:
        # telebot.apihelper.ApiTelegramException: A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message
        if previous_calculator_value != '':
            # prepare message
            if calculator_value == '':
                str_message = '0'
            else:
                if calculator_memory == '':
                    str_message = f'{calculator_value}'
                else:
                    str_message = f'{calculator_value} (память: {calculator_memory})'
            logging.debug(f'str_message = {str_message}')
            # send message
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=str_message, reply_markup=keyboard_layout)

#=======================================================


    # testing bot with simple echoing message object
    # @bot.message_handler(func=lambda message: True)
    # def echo_all(message):
    #     bot.reply_to(message, message.text)



    # starting the bot
    bot.infinity_polling()

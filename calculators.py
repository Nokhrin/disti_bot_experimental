# heads_and_heart_calculator
def heads_and_heart_calculator():
    result = 'калькулятор находится в разработке'
    return result

# temperature converter
def temperature_converter(degree, unit):
    # accepts Celsius and Fahrenheit
    degree_sign = u'\N{DEGREE SIGN}'

    if unit.lower() in ['f', 'ф']:
        result = f'{degree:.1f}{degree_sign} по Фаренгейту = '\
                 f'{(degree - 32) * 5 / 9:.1f}{degree_sign} по Цельсию'
        return result
    elif unit.lower() in ['c', 'с']:
        result = f'{degree:.1f}{degree_sign} по Цельсию = '\
                 f'{(degree * 9 / 5) + 32:.1f}{degree_sign} по Фаренгейту'
        return result
    else:
        return 'могу перевести из градусов Цельсия в градусы Фаренгейта и наоборот'

# simple math calculator
def simple_math_calculator(str_function, int_number_1, int_number_2):
    str_expression = f'{int_number_1} {str_function} {int_number_2}'
    str_result = eval(str_expression)
    return str_result

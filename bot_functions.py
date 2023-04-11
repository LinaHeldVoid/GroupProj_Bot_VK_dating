import configparser
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import common_functions


def kirillic_symbols():
    letters_permitted = ['АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя']
    kirillic = set(letters_permitted)
    return kirillic


def write_msg(session, user_id, message, keyboard=None):
    params = {
        'user_id': user_id,
        'message': message,
        'random_id': random.randrange(10 ** 7),
    }
    if keyboard is not None:
        params['keyboard'] = keyboard.get_keyboard()
    else:
        params = params

    session.method('messages.send', params)


def wrong_input(session, user_id):
    write_msg(session, user_id, 'Пожалуйста, выбери значение с кнопки, дорогуша.')


def keyboard_1_generate():
    keyboard_1 = VkKeyboard()
    keyboard_1.add_button('Вперёд!', VkKeyboardColor.POSITIVE)
    return keyboard_1


def keyboard_2_generate():
    keyboard_2 = VkKeyboard()
    keyboard_2.add_button('Парня', VkKeyboardColor.PRIMARY)
    keyboard_2.add_line()
    keyboard_2.add_button('Девушку', VkKeyboardColor.PRIMARY)
    keyboard_2.add_line()
    keyboard_2.add_button('Пол не важен', VkKeyboardColor.PRIMARY)
    return keyboard_2


def keyboard_3_generate():
    keyboard_3 = VkKeyboard()
    keyboard_3.add_button('Да! Добавь в Избранное', VkKeyboardColor.POSITIVE)
    keyboard_3.add_line()
    keyboard_3.add_button('Давай посмотрим ещё', VkKeyboardColor.PRIMARY)
    keyboard_3.add_line()
    keyboard_3.add_button('Нет. Больше не показывай', VkKeyboardColor.SECONDARY)
    keyboard_3.add_line()
    keyboard_3.add_button('Стоп', VkKeyboardColor.NEGATIVE)
    keyboard_3.add_line()
    return keyboard_3


def keyboard_4_generate():
    keyboard_4 = VkKeyboard()
    keyboard_4.add_button('Страна не имеет значения', VkKeyboardColor.PRIMARY)
    return keyboard_4


def keyboard_5_generate():
    keyboard_5 = VkKeyboard()
    keyboard_5.add_button('Город не имеет значения', VkKeyboardColor.PRIMARY)
    return keyboard_5


def keyboard_6_generate():
    keyboard_6 = VkKeyboard()
    keyboard_6.add_button('Поищем ещё!', VkKeyboardColor.POSITIVE)
    keyboard_6.add_line()
    keyboard_6.add_button('Заканчивай', VkKeyboardColor.POSITIVE)
    keyboard_6.add_line()
    return keyboard_6


def create_db():

    """ЗДЕСЬ ДОЛЖНА БЫТЬ ФУНКЦИЯ, СОЗДАЮЩАЯ ЯЧЕЙКУ ДЛЯ ПОЛЬЗОВАТЕЛЕ"""


def save_to_favorites():

    """ЗДЕСЬ ДОЛЖНА БЫТЬ ФУНКЦИЯ, СОХРАНЯЮЩАЯ ЧЕЛОВЕКА В ИЗБРАННЫЕ"""


def save_to_black_list():

    """ЗДЕСЬ ДОЛЖНА БЫТЬ ФУНКЦИЯ, КИДАЮЩАЯ ЧЕЛОВЕКА В ЧС"""

    """НЕ ЗАБУДЬТЕ УДАЛИТЬ ДАННЫЕ ИЗ CANDIDATES_LIST!!!"""


def clear_db():

    """ЗДЕСЬ ДОЛЖНА БЫТЬ ФУНКЦИЯ, УДАЛЯЮЩАЯ ИНФОРМАЦИЮ ИЗ БД"""


def bot_satisfied_reply():
    reply_list = [
        'Одобряю, дорогуша!',
        'Отличный выбор!',
        'Как скажешь))',
        'Не забудь написать своей паре!',
        'У тебя отличный вкус!',
        'Счастья молодым!',
        'Позови на свадьбу:)'
    ]
    reply = random.choice(reply_list)
    return reply


def bot_upset_reply():
    reply_list = [
        'Как жаль.',
        'Как пожелаешь.',
        'Ох. Хорошо, что человек не видит твоего ответа.',
        'Окей, сделано.',
        'Как жестоко(',
        'Суровый вердикт.',
        'Ладно-ладно.',
        'Хозяин-барин.',
        'Вредина('
    ]
    reply = random.choice(reply_list)
    return reply


def bot_neutral_reply():
    reply_list = [
        'Ладно.',
        'Окей!',
        'Я поняла, посмотрим ещё)',
        'Крутите барабан!',
        'Оки-доки:)',
        'Вредность твоя не знает границ ;)',
        'Тебе не угодишь!',
        'Хозяин-барин.',
        'Как пожелаешь, величество)',
        'Не то чтобы я запрограммирована уставать...'
    ]
    reply = random.choice(reply_list)
    return reply


def bot_next_reply():
    reply_list = [
        'Что насчёт этого?',
        'Полетели дальше!',
        'Следующий претендент!',
        'В студию!',
        'Следующий кандидат!',
        'Что тут у нас?',
        'Вот ещё, например.',
        'Что думаешь?',
        'Что скажешь?',
        'Каков твой вердикт?)'
    ]
    reply = random.choice(reply_list)
    return reply


def greetings(session, event, user_id):
    write_msg(session, user_id, 'Добро пожаловать в наш бот для знакомств! '
                                'Хочешь встретить свою судьбу?;)', keyboard_1_generate())
    while True:
        if event.text == 'Вперёд!':
            create_db()
            break
        else:
            wrong_input(session, user_id)
            continue


def gender_choice(session, event, user_id):
    write_msg(session, user_id, 'Приступим! Кого ты желаешь найти?', keyboard_2_generate())
    text = event.text
    while True:
        if text == 'Парня':
            gender = 2
        elif text == 'Девушку':
            gender = 1
        elif text == 'Пол не важен':
            gender = 0
        else:
            wrong_input(session, user_id)
            continue
        return gender


def age_check_low(session, user_id):
    while True:
        write_msg(session, user_id, 'Теперь поговорим про возраст партнёра.'
                                    'Какая нижняя граница желаемого возраста?')
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                if text is not None:
                    if text.isnumeric():
                        if text >= 12:
                            age_low = text
                        else:
                            write_msg(session, user_id, 'Извините, наш бот не может искать партнёров младше 12 лет.')
                            continue
                    else:
                        write_msg(session, user_id, 'Пожалуйста, введите ответ цифрой.')
                        continue
                else:
                    write_msg(session, user_id, 'Пожалуйста, введите ответ.')
                    continue
                return age_low


def age_check_high(session, user_id):
    while True:
        write_msg(session, user_id, 'Что насчёт верхней планки?')
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                if text is not None:
                    if text.isnumeric():
                        age_high = text
                    else:
                        write_msg(session, user_id, 'Пожалуйста, введите ответ цифрой.')
                        continue
                else:
                    write_msg(session, user_id, 'Пожалуйста, введите ответ.')
                    continue
                return age_high


def country_input(session, user_id):
    while True:
        write_msg(session, user_id, 'Отлично! В какой стране ищете вашего человека?', keyboard_4_generate())
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                if text is not None:
                    if text in kirillic_symbols():
                        if text == 'Страна не имеет значения':
                            country = 0
                        else:
                            country = text
                    else:
                        write_msg(session, user_id, 'Пожалуйста, введите ответ кириллицей.')
                        continue
                else:
                    write_msg(session, user_id, 'Пожалуйста, введите ответ.')
                    continue
                return country


def city_input(session, user_id):
    while True:
        write_msg(session, user_id, 'Теперь укажите желаемый город', keyboard_5_generate())
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                if text is not None:
                    if text in kirillic_symbols():
                        if text == 'Город не имеет значения':
                            city = 0
                        else:
                            city = text
                    else:
                        write_msg(session, user_id, 'Пожалуйста, введите ответ кириллицей.')
                        continue
                else:
                    write_msg(session, user_id, 'Пожалуйста, введите ответ.')
                    continue
                return city


def search_partner_list(session, user_id, age_low, age_high, gender, country, city):
    age_low = age_low
    age_high = age_high
    gender = gender
    country = country
    city = city

    """ЗДЕСЬ АКТИВИРУЕТСЯ ПОИСК"""

    candidate_list = []
    return candidate_list


def random_person(candidate_list):
    candidate = random.choice(candidate_list)
    return candidate


def discuss_candidates(session, user_id, candidate_list):
    candidate_list = candidate_list

    """ВЫВОДИТСЯ РАНДОМНЫЙ ЧЕЛОВЕК ИЗ ВЫБОРКИ"""

    write_msg(session, user_id, 'Начнём! Что думаешь об этом человеке?', keyboard_3_generate())
    while True:
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                if text == 'Да! Добавь в Избранное':
                    bot_satisfied_reply()
                    save_to_favorites()
                    bot_next_reply()
                    random_person(candidate_list)
                elif text == 'Давай посмотрим ещё':
                    bot_neutral_reply()
                    bot_next_reply()
                    random_person(candidate_list)
                    continue
                elif text == 'Нет. Больше не показывай':
                    bot_upset_reply()
                    save_to_black_list()
                    bot_next_reply()
                    random_person(candidate_list)
                    continue
                elif text == 'Стоп':
                    break
                else:
                    wrong_input(session, user_id)
                    continue


def final_menu(session, user_id, candidate_list):
    write_msg(session, user_id, 'Что хочешь делать сейчас, дорогуша?', keyboard_6_generate())
    while True:
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                if text == 'Поищем ещё!':
                    write_msg(session, user_id, 'Вот это настрой! Я в тебе не сомневалась)', keyboard_1_generate())
                    discuss_candidates(session, user_id, candidate_list)
                    decision = 1
                elif text == 'Заканчивай':
                    write_msg(session, user_id, 'Я поняла тебя! Дай знать, если захочешь вернуться;)', keyboard_1_generate())
                    decision = 0
                else:
                    wrong_input(session, user_id)
                    continue
                return decision
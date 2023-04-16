import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType


import common_functions


def kirillic_symbols(text):
    letters_permitted = 'АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    kirillic = list(letters_permitted)
    example = list(text)
    for letter in example:
        if letter not in kirillic:
            return False
    return True


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
    write_msg(session, user_id, "Пожалуйста, выбери значение с кнопки, дорогуша.")


def keyboard_hello_generate():
    keyboard_hello = VkKeyboard()
    keyboard_hello.add_button('Вперёд!', VkKeyboardColor.POSITIVE)
    return keyboard_hello


def keyboard_gender_generate():
    keyboard_gender = VkKeyboard()
    keyboard_gender.add_button('Парня', VkKeyboardColor.PRIMARY)
    keyboard_gender.add_line()
    keyboard_gender.add_button('Девушку', VkKeyboardColor.PRIMARY)
    keyboard_gender.add_line()
    keyboard_gender.add_button('Пол не важен', VkKeyboardColor.PRIMARY)
    return keyboard_gender


def keyboard_stupid_generate():
    keyboard_stupid = VkKeyboard()
    keyboard_stupid.add_button('Введи число с клавиатуры', VkKeyboardColor.SECONDARY)
    return keyboard_stupid


def keyboard_discussion_generate():
    keyboard_discussion = VkKeyboard()
    keyboard_discussion.add_button('Да! Добавь в Избранное', VkKeyboardColor.POSITIVE)
    keyboard_discussion.add_line()
    keyboard_discussion.add_button('Давай посмотрим ещё', VkKeyboardColor.PRIMARY)
    keyboard_discussion.add_line()
    keyboard_discussion.add_button('Нет. Больше не показывай', VkKeyboardColor.SECONDARY)
    keyboard_discussion.add_line()
    keyboard_discussion.add_button('Стоп', VkKeyboardColor.NEGATIVE)
    return keyboard_discussion


def keyboard_country_generate():
    keyboard_country = VkKeyboard()
    keyboard_country.add_button('Страна не имеет значения', VkKeyboardColor.PRIMARY)
    return keyboard_country


def keyboard_city_generate():
    keyboard_city = VkKeyboard()
    keyboard_city.add_button('Город не имеет значения', VkKeyboardColor.PRIMARY)
    return keyboard_city


def keyboard_final_generate():
    keyboard_final = VkKeyboard()
    keyboard_final.add_button('Поищем ещё!', VkKeyboardColor.POSITIVE)
    keyboard_final.add_line()
    keyboard_final.add_button('Заканчивай', VkKeyboardColor.POSITIVE)
    return keyboard_final



def create_db():
    pass


def save_to_favorites():
    pass


def save_to_black_list():
    pass


def clear_db():
    pass


def bot_satisfied_reply():
    pass


def bot_upset_reply():
    pass


def bot_neutral_reply():
    pass


def bot_next_reply():
    pass


def greetings(session, user_id):
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            write_msg(session, user_id, 'Добро пожаловать в наш бот для знакомств! '
                                        'Хочешь встретить свою судьбу?;)', keyboard_hello_generate())
            return


def start_bot(session, user_id):
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Вперёд!':
                create_db()
                return
            else:
                wrong_input(session, user_id)


def gender_choice(session, user_id):
    write_msg(session, user_id, 'Приступим! Кого ты желаешь найти?', keyboard_gender_generate())
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text == 'Парня':
                gender = 2
                return gender
            elif text == 'Девушку':
                gender = 1
                return gender
            elif text == 'Пол не важен':
                gender = 0
                return gender
            else:
                wrong_input(session, user_id)


def age_check_low(session, user_id):
    write_msg(session, user_id, 'Теперь поговорим про возраст партнёра. '
                                'Какая нижняя граница желаемого возраста?', keyboard_stupid_generate())
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text is not None:
                if text.isnumeric():
                    text = int(text)
                    if text >= 12:
                        age_low = text
                        return age_low
                    else:
                        write_msg(session, user_id, 'Извини, наш бот не может искать партнёров младше 12 лет.')
                else:
                    write_msg(session, user_id, 'Пожалуйста, введи ответ цифрой.')
            else:
                write_msg(session, user_id, 'Пожалуйста, введи ответ.')


def age_check_high(session, user_id, age_low):
    write_msg(session, user_id, 'Что насчёт верхней планки?', keyboard_stupid_generate())
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text is not None:
                if text.isnumeric():
                    text = int(text)
                    if text <= age_low:
                        write_msg(session, user_id, 'Бот умеет считать, дорогуша) '
                                                    'Этот показатель должен быть БОЛЬШЕ, чем предыдущий.')
                    else:
                        age_high = text
                        return age_high
                else:
                    write_msg(session, user_id, 'Пожалуйста, введи ответ цифрой.')
            else:
                write_msg(session, user_id, 'Пожалуйста, введи ответ.')


def country_input(session, user_id):
    write_msg(session, user_id, 'Отлично! В какой стране ищете вашего человека?', keyboard_country_generate())
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text is not None:
                if kirillic_symbols(text):
                    if text == 'Страна не имеет значения':
                        country = None
                        return country
                    else:
                        country = text
                        return country
                else:
                    write_msg(session, user_id, 'Пожалуйста, введите ответ кириллицей.')
            else:
                write_msg(session, user_id, 'Пожалуйста, введите ответ.')


def city_input(session, user_id):
    write_msg(session, user_id, 'Теперь укажите желаемый город', keyboard_city_generate())
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text is not None:
                if kirillic_symbols(text):
                    if text == 'Город не имеет значения':
                        city = 0
                        return city
                    else:
                        city = text
                        return city
                else:
                    write_msg(session, user_id, 'Пожалуйста, введи ответ кириллицей.')
            else:
                write_msg(session, user_id, 'Пожалуйста, введи ответ.')


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

    write_msg(session, user_id, 'Начнём! Что думаешь об этом человеке?', keyboard_discussion_generate())
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
            elif text == 'Нет. Больше не показывай':
                bot_upset_reply()
                save_to_black_list()
                bot_next_reply()
                random_person(candidate_list)
            elif text == 'Стоп':
                return
            else:
                wrong_input(session, user_id)


def final_menu(session, user_id):
    write_msg(session, user_id, 'Что хочешь делать сейчас, дорогуша?', keyboard_final_generate())
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text == 'Поищем ещё!':
                write_msg(session, user_id, 'Вот это настрой! Я в тебе не сомневалась)')
                decision = 1
                return decision
            elif text == 'Заканчивай':
                write_msg(session, user_id, 'Я поняла тебя! Дай знать, если захочешь вернуться;)',
                          keyboard_hello_generate())
                decision = 0
                return decision
            else:
                wrong_input(session, user_id)


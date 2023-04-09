import configparser
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import common_functions


config = configparser.ConfigParser()
config.read("TOKENS_DANGER.ini")
token = config['VK']['bot_token']

session = vk_api.VkApi(token=token)


def write_msg(user_id, message, keyboard=None):
    params = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }
    if keyboard != None:
        params['keyboard'] = keyboard.get_keyboard()
    else:
        params = params

    session.method('messages.send', params)


def location(user_id):
    write_msg(user_id, 'Отлично! Теперь укажите ваш город.'
                       'Если локация для вас не важна, напишите "не важно"')
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text == 'не важно' or text == 'Не важно':
                city = 0
            else:
                city = text
            return city


for event in VkLongPoll(session).listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text
        user_id = event.user_id

        if text == 'привет' or text == 'Привет':
            keyboard_1 = VkKeyboard()
            keyboard_1.add_button('Вперёд!', VkKeyboardColor.POSITIVE)

            write_msg(user_id, 'Вы готовы встретиться со своей судьбой?)', keyboard_1)

        elif text == 'Вперёд!':
            keyboard_2 = VkKeyboard()
            keyboard_2.add_button('Парня', VkKeyboardColor.PRIMARY)
            keyboard_2.add_line()
            keyboard_2.add_button('Девушку', VkKeyboardColor.PRIMARY)
            keyboard_2.add_line()
            keyboard_2.add_button('Пол не важен', VkKeyboardColor.PRIMARY)

            write_msg(user_id, 'Кого вы ищете?', keyboard_2)

        elif text == 'Парня':
            gender = '2'
            location = location(user_id)
        elif text == 'Девушку':
            gender = '1'
            location = location(user_id)
        elif text == 'Пол не важен':
            gender = '0'
            location = location(user_id)


        else:
            write_msg(user_id, 'Извините, ваш ответ не распознан. Напишите боту "привет" для начала поиска')

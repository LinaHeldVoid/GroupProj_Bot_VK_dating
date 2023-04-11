import configparser
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


config = configparser.ConfigParser()
config.read("token_list.ini")
token = config["VK"]["bot_token"]

session = vk_api.VkApi(token=token)


def write_msg(user_id, message, keyboard=None):
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": randrange(10**7),
    }
    if keyboard != None:
        params["keyboard"] = keyboard.get_keyboard()

    session.method("messages.send", params)


def location(user_id):
    write_msg(
        user_id,
        'Отлично! Теперь укажите ваш город. Если локация для вас не важна, напишите "не важно"',
    )
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text.lower() == "не важно":
                city = 0
            else:
                city = text
            return city


for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text
        user_id = event.user_id

        if text.lower() == "привет":
            keyboard_1 = VkKeyboard()
            keyboard_1.add_button("Вперёд!", VkKeyboardColor.POSITIVE)

            write_msg(user_id, "Вы готовы встретиться со своей судьбой?)", keyboard_1)

        elif text.lower() == "вперёд!":
            keyboard_2 = VkKeyboard()
            keyboard_2.add_button("Парня", VkKeyboardColor.PRIMARY)
            keyboard_2.add_line()
            keyboard_2.add_button("Девушку", VkKeyboardColor.PRIMARY)
            keyboard_2.add_line()
            keyboard_2.add_button("Пол не важен", VkKeyboardColor.PRIMARY)

            write_msg(user_id, "Кого вы ищете?", keyboard_2)

        elif text.lower() == "парня":
            gender = "2"
            location = location(user_id)
            write_msg(user_id, f"Вы выбрали: парня, город: {location}")

        elif text.lower() == "девушку":
            gender = "1"
            location = location(user_id)
            write_msg(user_id, f"Вы выбрали: девушку, город: {location}")

        elif text.lower() == "пол не важен":
            gender = "0"
            location = location(user_id)
            write_msg(user_id, f"Вы выбрали: пол не важен, город: {location}")

        else:
            write_msg(
                user_id,
                'Извините, ваш ответ не распознан. Напишите боту "привет" для начала поиска',
            )

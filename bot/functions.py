import configparser
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import keyboard


def write_msg(self, user_id, message, keyboard=None):
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": random.randrange(10**7),
    }
    if keyboard is not None:
        params["keyboard"] = keyboard.get_keyboard()
    else:
        params = params

    session.method("messages.send", params)


def wrong_input(session, user_id):
    write_msg(session, user_id, "Пожалуйста, выбери значение с кнопки, дорогуша.")


def greetings(session, event, user_id):
    write_msg(
        session,
        user_id,
        "Добро пожаловать в наш бот для знакомств! " "Хочешь встретить свою судьбу?;)",
        keyboard_1_generate(),
    )
    while True:
        if event.text == "Вперёд!":
            create_db()
            break
        else:
            wrong_input(session, user_id)
            continue


def gender_choice(session, event, user_id):
    write_msg(
        session, user_id, "Приступим! Кого ты желаешь найти?", keyboard_2_generate()
    )
    text = event.text
    while True:
        if text == "Парня":
            gender = 2
        elif text == "Девушку":
            gender = 1
        elif text == "Пол не важен":
            gender = 0
        else:
            wrong_input(session, user_id)
            continue
        return gender


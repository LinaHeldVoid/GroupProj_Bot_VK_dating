import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# удаляем функцию kirillic_symbols, которая не используется в коде

def write_msg(session, user_id, message, keyboard=None):
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": random.randrange(10**7),
    }
    if keyboard is not None:
        params["keyboard"] = keyboard.get_keyboard()
    # else: # else тут не нужен, так как он ничего не делает
    session.method("messages.send", params)


def wrong_input(session, user_id):
    write_msg(session, user_id, "Пожалуйста, выбери значение с кнопки, дорогуша.")


def start_button():
    keyboard_1 = VkKeyboard()
    keyboard_1.add_button("Вперёд!", VkKeyboardColor.POSITIVE)
    return keyboard_1


def gender_button():
    keyboard_2 = VkKeyboard()
    keyboard_2.add_button("Парня", VkKeyboardColor.PRIMARY)
    keyboard_2.add_line()
    keyboard_2.add_button("Девушку", VkKeyboardColor.PRIMARY)
    keyboard_2.add_line()
    keyboard_2.add_button("Пол не важен", VkKeyboardColor.PRIMARY)
    return keyboard_2


# удаляем неиспользуемые функции keyboard_3_generate(), keyboard_4_generate(),
# keyboard_5_generate() и keyboard_6_generate()

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


def greetings(session, event, user_id):
    write_msg(
        session,
        user_id,
        "Добро пожаловать в наш бот для знакомств! " "Хочешь встретить свою судьбу?;)",
        start_button(),
    )
    # вместо цикла while в функции greetings() используем условный оператор if-else,
    # чтобы проверить, что текст сообщения равен "Вперёд!"
    if event.text == "Вперёд!":
        create_db()
    else:
        wrong_input(session, user_id)


def gender_choice(session, event, user_id):
    write_msg(
        session, user_id, "Приступим! Кого ты желаешь найти?", gender_button()
    )
    # вместо цикла while в функции gender_choice() используем условный оператор if-elif-else,
    # чтобы проверить, что текст сообщения равен "Парня", "Девушку" или "Пол не важен"
    if event.text == "Парня":
        gender = 2
    elif event.text == "Девушку":
        gender = 1
    elif event.text == "Пол не важен":
        gender = 0
    else:
        wrong_input(session, user_id)
        gender = None # возвращаем None, если значение не выбрано
    return gender



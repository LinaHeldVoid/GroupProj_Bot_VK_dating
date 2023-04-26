import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from bot.keyboard import *
from db.db_functions import *
from vk.user_information import take_user_info, VK


def kirillic_symbols(text):
    letters_permitted = (
        "АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя -"
    )
    kirillic = list(letters_permitted)
    example = list(text)
    for letter in example:
        if letter not in kirillic:
            return False
    return True


def write_msg(session, user_id, message, keyboard=None):
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": random.randrange(10**7),
    }
    if keyboard is not None:
        params["keyboard"] = keyboard.get_keyboard()
    session.method("messages.send", params)


def wrong_input(session, user_id):
    write_msg(session, user_id, "Пожалуйста, выбери значение с кнопки, дорогуша.")


def greetings(session, user_id):
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            who = take_user_info(user_id)
            write_msg(
                session,
                user_id,
                f"Привет, {who['first_name']}! Добро пожаловать в наш бот для знакомств.\n"
                f"Исходя из данных о тебе: город: {who['city_title']}, возраст: {who['age']} лет\n"
                f"Подберём тебе пару.\n\n"
                f"Жми кнопку Вперёд и начнём",
                keyboard_hello_generate(),
            )
            return


def start_bot(session, user_id):
    create_db()
    create_table()
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Вперёд!":
                return
            else:
                wrong_input(session, user_id)


def gender_choice(session, user_id):
    write_msg(
        session,
        user_id,
        "Приступим! Кого ты желаешь найти?",
        keyboard_gender_generate(),
    )
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text == "Парня":
                gender = 2
                return gender
            elif text == "Девушку":
                gender = 1
                return gender
            elif text == "Пол не важен":
                gender = 0
                return gender
            else:
                wrong_input(session, user_id)


def age_check_low(session, user_id):
    write_msg(
        session,
        user_id,
        "Теперь поговорим про возраст партнёра. "
        "Какая нижняя граница желаемого возраста?",
        keyboard_stupid_generate(),
    )
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
                        write_msg(
                            session,
                            user_id,
                            "Извини, наш бот не может искать партнёров младше 12 лет.",
                        )
                else:
                    write_msg(session, user_id, "Пожалуйста, введи ответ цифрой.")
            else:
                write_msg(session, user_id, "Пожалуйста, введи ответ.")


def age_check_high(session, user_id, age_low):
    write_msg(
        session, user_id, "Что насчёт верхней планки?", keyboard_stupid_generate()
    )
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text is not None:
                if text.isnumeric():
                    text = int(text)
                    if text < age_low:
                        write_msg(
                            session,
                            user_id,
                            "Бот умеет считать, дорогуша) "
                            "Этот показатель должен быть БОЛЬШЕ, чем предыдущий.",
                        )
                    else:
                        age_high = text
                        return age_high
                else:
                    write_msg(session, user_id, "Пожалуйста, введи ответ цифрой.")
            else:
                write_msg(session, user_id, "Пожалуйста, введи ответ.")


"""ЗДЕСЬ АКТИВИРУЕТСЯ ПОИСК (см. VK.search_candidates)"""


def random_person(candidate_list):
    candidate = random.choice(candidate_list)
    return candidate


"""ВЫВОДИТСЯ РАНДОМНЫЙ ЧЕЛОВЕК ИЗ ВЫБОРКИ"""


def get_random_candidate(cur):
    cur.execute(
        """
            SELECT p.first_name, p.last_name, p.vk_id, p.vk_link 
            FROM people_found p 
            LEFT JOIN black_list b ON p.black_list_id = b.black_list_id 
            WHERE b.black_list_id IS NULL 
            ORDER BY random() LIMIT 1
        """
    )
    candidate_data = cur.fetchone()
    fname = candidate_data[0]
    lname = candidate_data[1]
    vk_id = candidate_data[2]
    link = candidate_data[3]
    vk = VK()
    photos = vk.data_for_db(vk_id)
    return fname, lname, photos, link


def get_people_from_favorites(cur):
    cur.execute(
        """
        SELECT p.*
        FROM people_found p
        JOIN favorites f ON p.favorit_id = f.favorit_id;
    """
    )
    result = cur.fetchall()
    message = "\n".join([str(row) for row in result])
    return message


def message_generator(session, user_id, cur):
    fname, lname, photo, link = get_random_candidate(cur)
    message = f"{fname} {lname}\n\n{link}"
    for pics in photo:
        write_msg(
            session,
            user_id,
            f"\n{pics}",
        )
        print(pics)
    write_msg(
        session,
        user_id,
        f"\n{message}",
        keyboard_discussion_generate(),
    )
    return fname, lname, link


async def discuss_candidates(session, user_id):
    conn = psycopg2.connect(
        host="localhost", user="postgres", password="postgres", database="vkinder"
    )
    cur = conn.cursor()
    fname, lname, link = message_generator(session, user_id, cur)
    write_msg(
        session,
        user_id,
        f"Начнём! Что думаешь об этом человеке?",
    )
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text == "Да! Добавь в Избранное":
                save_to_favorites(cur, conn, fname, lname, link)
                write_msg(
                    session,
                    user_id,
                    f"Что думаешь об этом человеке?"
                )
                fname, lname, link = message_generator(session, user_id, cur)
            elif text == "Давай посмотрим ещё":
                save_to_favorites(cur, conn, fname, lname, link)
                write_msg(
                    session,
                    user_id,
                    f"Что думаешь об этом человеке?"
                )
                fname, lname, link = message_generator(session, user_id, cur)
            elif text == "Нет. Больше не показывай":
                save_to_black_list(cur, conn, fname, lname, link)
                save_to_favorites(cur, conn, fname, lname, link)
                write_msg(
                    session,
                    user_id,
                    f"Что думаешь об этом человеке?"
                )
                fname, lname, link = message_generator(session, user_id, cur)
            elif text == "Стоп":
                return
            else:
                wrong_input(session, user_id)


def final_menu(session, user_id):
    conn = psycopg2.connect(
        host="localhost", user="postgres", password="postgres", database="vkinder"
    )
    cur = conn.cursor()
    write_msg(
        session,
        user_id,
        "Что хочешь делать сейчас, дорогуша?",
        keyboard_final_generate(),
    )
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            if text == "Поищем ещё!":
                write_msg(session, user_id, "Вот это настрой! Я в тебе не сомневалась)")
                decision = 1
                return decision
            elif text == "Покажи моих Избранных":
                try:
                    message = get_people_from_favorites(cur)
                    write_msg(session, user_id, message)
                except vk_api.exceptions.ApiError as e:
                    if e.code == 100:
                        write_msg(session, user_id, "Список 'Избранных' пуст.")
                        continue
                    else:
                        raise e
            elif text == "Заканчивай":
                write_msg(
                    session,
                    user_id,
                    "Я поняла тебя! Дай знать, если захочешь вернуться;)",
                    keyboard_hello_generate(),
                )
                decision = 0
                return decision
            else:
                wrong_input(session, user_id)

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.db import vkinder_bd


def create_db():
    try:
        conn = psycopg2.connect(
            host="localhost", user="postgres", password="postgres", port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        sql_create_database = "create database VKinder"
        cursor.execute(sql_create_database)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")


def create_table():
    try:
        conn = psycopg2.connect(
            host="localhost", user="postgres",
            password="postgres", port=5432,
            database="vkinder"
        )
        cursor = conn.cursor()
        cursor.execute(vkinder_bd)
        conn.commit()
        print("Таблица успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")


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

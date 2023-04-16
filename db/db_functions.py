import psycopg2
from db.db import create_tables


def create_db():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port=5432
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        # Проверяем наличие базы данных
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'VKinder'")
        exists = cur.fetchone()
        if exists:
            print('База данных уже существует')
        else:
            # Создаем базу данных
            cur.execute("CREATE DATABASE VKinder")
    conn.autocommit = False
    create_tables(conn)
    conn.close()





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

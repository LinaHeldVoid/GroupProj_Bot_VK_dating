import psycopg2
from db.db import create_tables


def create_db():
    with psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres",
            port=5432
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
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

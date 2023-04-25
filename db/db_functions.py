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
            host="localhost",
            user="postgres",
            password="postgres",
            port=5432,
            database="vkinder",
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


# Удаляем все записи из таблицы people_found / обнуляем таблицу перед новым поиском
def drop_tables_data():
    conn = psycopg2.connect(
        host="localhost", user="postgres", password="postgres", database="vkinder"
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM people_found")
    conn.commit()


def save_to_favorites(cur, conn, fname, lname, link):
    # Найти id записи из таблицы people_found
    cur.execute(
        "SELECT id FROM people_found WHERE first_name = %s AND last_name = %s",
        (fname, lname),
    )
    person_id = cur.fetchone()[0]
    # Вставить новую запись в таблицу favorites
    cur.execute(
        "INSERT INTO favorites (vk_link) VALUES (%s) RETURNING favorit_id", (link,)
    )
    favorit_id = cur.fetchone()[0]
    # Обновить запись в таблице people_found
    cur.execute(
        "UPDATE people_found SET favorit_id = %s WHERE id = %s", (favorit_id, person_id)
    )
    conn.commit()


def save_to_black_list(cur, conn, fname, lname, link):
    # Найти id записи из таблицы people_found
    cur.execute(
        "SELECT id FROM people_found WHERE first_name = %s AND last_name = %s",
        (fname, lname),
    )
    person_id = cur.fetchone()[0]
    # Вставить новую запись в таблицу black_list
    cur.execute(
        "INSERT INTO black_list (vk_link) VALUES (%s) RETURNING black_list_id", (link,)
    )
    black_list_id = cur.fetchone()[0]
    # Обновить запись в таблице people_found
    cur.execute(
        "UPDATE people_found SET black_list_id = %s WHERE id = %s",
        (black_list_id, person_id),
    )
    conn.commit()

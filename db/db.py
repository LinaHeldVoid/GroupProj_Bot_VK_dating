import psycopg2

conn = psycopg2.connect(
    host="host", user="user", password="password", database="VKinder"
)
# создание курсора
cur = conn.cursor()


# функция для создания таблицы users
def create_users_table(cur):
    cur.execute(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            vk_id INT,
            vk_link VARCHAR(100),
            city VARCHAR(50),
            favorit_id INT REFERENCES favorites(favorit_id),
            black_list_id INT REFERENCES black_list(black_list_id)
            candidates_id INT REFERENCES candidates(candidates_id)
        )
    """
    )


# функция для создания таблицы favorites
def create_favorites_table(cur):
    cur.execute(
        """
        CREATE TABLE favorites (
            favorit_id SERIAL PRIMARY KEY,
            vk_link VARCHAR(100)
        )
    """
    )


# функция для создания таблицы black_list
def create_black_list_table(cur):
    cur.execute(
        """
        CREATE TABLE black_list (
            black_list_id SERIAL PRIMARY KEY,
            vk_link VARCHAR(100)
        )
    """
    )

# функция для создания таблицы candidates

def create_candidates(cur):
    cur.execute(
        """
        CREATE TABLE candidates (
            candidates_id SERIAL PRIMARY KEY,
            vk_link VARCHAR(100)
        )
    """
    )


if __name__ == "__main__":
    create_favorites_table()
    create_black_list_table()
    create_users_table()
    create_candidates()
def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                vk_id INT,
                vk_link VARCHAR(100),
                city VARCHAR(50),
                favorit_id INT REFERENCES favorites(favorit_id),
                black_list_id INT REFERENCES black_list(black_list_id),
                candidates_id INT REFERENCES candidates(candidates_id)
            );
            CREATE TABLE IF NOT EXISTS favorites (
                favorit_id SERIAL PRIMARY KEY,
                vk_link VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS black_list (
                black_list_id SERIAL PRIMARY KEY,
                vk_link VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS candidates (
                candidates_id SERIAL PRIMARY KEY,
                vk_link VARCHAR(100)
            );
            """
        )
        conn.commit()

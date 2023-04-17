vkinder_bd = """CREATE TABLE favorites (
    favorit_id SERIAL PRIMARY KEY,
    vk_link VARCHAR(100)
);

CREATE TABLE black_list (
    black_list_id SERIAL PRIMARY KEY,
    vk_link VARCHAR(100)
);

CREATE TABLE candidates (
    candidates_id SERIAL PRIMARY KEY,
    vk_link VARCHAR(100)
);

CREATE TABLE users (
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
"""

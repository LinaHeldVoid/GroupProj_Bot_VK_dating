vkinder_bd = """
CREATE TABLE IF NOT EXISTS favorites (
    favorit_id SERIAL PRIMARY KEY,
    vk_link VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS black_list (
    black_list_id SERIAL PRIMARY KEY,
    vk_link VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS people_found (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    photo VARCHAR(500),
    vk_id INT,
    vk_link VARCHAR(300),
    favorit_id INT,
    black_list_id INT,
    CONSTRAINT fk_people_found_favorites FOREIGN KEY (favorit_id) REFERENCES favorites (favorit_id) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_people_found_black_list FOREIGN KEY (black_list_id) REFERENCES black_list (black_list_id) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    vk_id INT,
    vk_link VARCHAR(100),
    favorit_id INT REFERENCES favorites (favorit_id) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED,
    black_list_id INT REFERENCES black_list (black_list_id) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);
"""

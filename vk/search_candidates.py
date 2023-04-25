from data.token_list import access_token as token
import psycopg2
import vk_api
from vk.user_information import take_user_info
from bot.functions import write_msg


async def search_partner_list(session, user_id, age_low, age_high, gender):
    write_msg(
        session,
        user_id,
        f"Пожалуйста подождите осуществляю поиск. \nБип буп боп ╚═། ◑ ▃ ◑ །═╝",
    )
    conn = psycopg2.connect(
        host="localhost", user="postgres", password="postgres", database="vkinder"
    )
    cur = conn.cursor()
    # Удаляем все записи из таблиц/ обнуляем таблицы перед новым поиском
    cur.execute("DELETE FROM people_found")
    cur.execute("DELETE FROM favorites")
    cur.execute("DELETE FROM black_list")
    conn.commit()

    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    age_low = age_low
    age_high = age_high
    gender_FM0 = gender
    sex = 1 if gender_FM0 == 1 else 2
    # Определяем город
    city_id = take_user_info(user_id)["city"]
    # Определяем возрастные ограничения для поиска
    age_from = age_low
    age_to = age_high

    # Получаем первые 50 id пользователей, удовлетворяющих нашим критериям
    users_search = vk.users.search(
        city=city_id,
        sex=sex,
        age_from=age_from,
        age_to=age_to,
        fields="id",
        count=1000,
    )

    # Список id пользователей
    users_ids = [user["id"] for user in users_search["items"]]

    # Список id пользователей, у которых есть фотографии профиля
    users_with_photos_ids = []

    for user_id in users_ids:
        try:
            photos_search = vk.photos.get(owner_id=user_id, album_id="profile", count=1)
            if photos_search["count"] > 0:
                users_with_photos_ids.append(user_id)
        except vk_api.exceptions.ApiError as e:
            if e.code == 30:
                # Профиль закрытый, игнорируем его
                continue
            else:
                # Не удалось получить фотографии из профиля по другой причине
                raise e

    # Получаем информацию о пользователях, у которых есть фотографии профиля
    users_info = vk.users.get(
        user_ids=users_with_photos_ids,
        fields="id, first_name, last_name, photo_max_orig",
    )

    # Составляем список словарей, каждый словарь представляет отдельного пользователя
    candidate_list = []
    for user in users_info:
        candidate = {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "photo": user["photo_max_orig"],
        }
        candidate_list.append(candidate)

    # Сохраняем список кандидатов в базу данных
    for candidate in candidate_list:
        cur.execute(
            """
            INSERT INTO people_found (first_name, last_name, photo, vk_id, vk_link)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                candidate["first_name"],
                candidate["last_name"],
                f'{candidate["photo"]}',
                candidate["id"],
                f"https://vk.com/id{candidate['id']}",
            ),
        )
    conn.commit()

    return candidate_list

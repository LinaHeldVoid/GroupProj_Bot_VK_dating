from data.token_list import access_token as token
import psycopg2
import vk_api


def search_partner_list(session, user_id, age_low, age_high, gender, country, city):
    conn = psycopg2.connect(
        host="localhost", user="postgres", password="postgres", database="vkinder"
    )
    cur = conn.cursor()
    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    age_low = age_low
    age_high = age_high
    gender = gender
    country = country
    city = city
    sex = 1 if gender == 'Женский' else 2
    # Определяем город
    city_id = vk.database.getCities(country_id=1, q=city)['items'][0]['id']
    # Определяем возрастные ограничения для поиска
    age_from = age_low
    age_to = age_high

    # Получаем все id пользователей, удовлетворяющих нашим критериям
    users_search = vk.users.search(
        country=1,
        city=city_id,
        sex=sex,
        age_from=age_from,
        age_to=age_to,
        fields='id',
        count=1000
    )

    # Список id пользователей
    users_ids = [user['id'] for user in users_search['items']]

    # Список id пользователей, у которых есть фотографии профиля
    users_with_photos_ids = []

    for user_id in users_ids:
        try:
            photos_search = vk.photos.get(owner_id=user_id, album_id='profile', count=1)
            if photos_search['count'] > 0:
                users_with_photos_ids.append(user_id)
        except vk_api.exceptions.ApiError as e:
            if e.code == 30:
                # Профиль закрытый, игнорируем его
                continue
            else:
                # Не удалось получить фотографии из профиля по другой причине
                raise e

    # Получаем информацию о пользователях, у которых есть фотографии профиля
    users_info = vk.users.get(user_ids=users_with_photos_ids, fields='id, first_name, last_name, photo_max_orig')

    # Составляем список словарей, каждый словарь представляет отдельного пользователя
    candidate_list = []
    for user in users_info:
        candidate = {
            'id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'photo': user['photo_max_orig']
        }
        candidate_list.append(candidate)

    # Сохраняем список кандидатов в базу данных
    for candidate in candidate_list:
        cur.execute(
            """
            INSERT INTO candidates (vk_link)
            VALUES (%s)
            """,
            (f"<https://vk.com/id{candidate['id']}>",)
        )
    conn.commit()

    return candidate_list

# Функция для поиска пользователей VK по параметрам возраста, пола и города:
def search_users_vk(age_from: int, age_to: int, gender: int, city: int, vk_api: VK) -> list:
    params = {
        'age_from': age_from,
        'age_to': age_to,
        'sex': gender,
        'city': city,
        'count': 1000,  # Максимальное количество найденных пользователей
        'fields': 'photo_max_orig',
        'has_photo': 1,  # Искать только пользователей с фотографиями
        'sort': 0  # 0 - сортировка по релевантности, 1 - по дате регистрации, 2 - по популярности
    }

    search_url = 'https://api.vk.com/method/users.search'
    response = vk_api.make_request(search_url, params)
    return response['response']['items']

# Функция для получения топ-3 фотографий пользователя VK:
def get_top_3_photos_vk(user_id: int, vk_api: VK) -> list:
    photos_url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'count': 100,
        'rev': 1  # Сортировать по убыванию даты добавления
    }
    response = vk_api.make_request(photos_url, params)
    photos = response['response']['items']
    top_photos = nlargest(3, photos, key=lambda x: x['likes']['count'])
    return top_photos

# Функция для вывода информации о пользователе VK и его топ-3 фотографиях
# в формате, который можно отправить через API VK:
def send_user_info(user_id: int, user_name: str, vk_link: str, top_photos: list, vk_api: VK):
    message = f"Имя: {user_name}\nСсылка на профиль: {vk_link}"
    attachment = ",".join([f"photo{photo['owner_id']}_{photo['id']}" for photo in top_photos])
    vk_api.send_message(user_id, message, attachment)

# Функция для получения информации о пользователе VK по его ссылке:
def get_user_info_by_link(link: str, vk_api: VK) -> dict:
    params = {
        'user_ids': link,
        'fields': 'photo_max_orig'
    }
    search_url = 'https://api.vk.com/method/users.get'
    response = vk_api.make_request(search_url, params)
    return response['response'][0]

# Функция для добавления пользователя в список избранных:
def add_user_to_favorites(user_id: int, favorites_list: list) -> list:
    if user_id not in favorites_list:
        favorites_list.append(user_id)
    return favorites_list
# Функция для вывода списка избранных пользователей:
def show_favorites_list(favorites_list: list, vk_api: VK):
    if not favorites_list:
        vk_api.send_message("Your favorites list is empty.")
    else:
        message = "Your favorites list:\n\n"
        for index, favorite in enumerate(favorites_list):
            message += f"{index + 1}. {favorite}\n"
        vk_api.send_message(message)

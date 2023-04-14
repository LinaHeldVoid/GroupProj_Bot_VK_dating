import requests
from data.token_list import bot_token as token


def get_country_id(country_name):
    url = "<https://api.vk.com/method/database.getCountries>"
    params = {
        "q": country_name,
        "need_all": 0,
        "count": 1,
        "access_token": token,
        "v": "5.103",
    }
    response = requests.get(url, params=params)
    country_id = response.json()["response"]["items"][0]["id"]
    return country_id


def get_city_id(city_name, country_id):
    url = "<https://api.vk.com/method/database.getCities>"
    params = {
        "q": city_name,
        "country_id": country_id,
        "need_all": 0,
        "count": 1,
        "access_token": token,
        "v": "5.103",
    }
    response = requests.get(url, params=params)
    city_id = response.json()["response"]["items"][0]["id"]
    return city_id


def get_users_list(age_low, age_high, gender, city_id, country_id):
    url = "<https://api.vk.com/method/users.search>"
    params = {
        "age_from": age_low,
        "age_to": age_high,
        "sex": gender,
        "city": city_id,
        "country": country_id,
        "access_token": token,
        "v": "5.103",
    }
    response = requests.get(url, params=params)
    users_list = response.json()["response"]["items"]
    return users_list


def is_user_online(user_id):
    url = "<https://api.vk.com/method/users.get>"
    params = {
        "user_ids": user_id,
        "fields": "online",
        "access_token": token,
        "v": "5.103",
    }
    response = requests.get(url, params=params)
    is_online = response.json()["response"][0]["online"]
    return is_online


def add_to_friends(user_id):
    url = "<https://api.vk.com/method/friends.add>"
    params = {"user_id": user_id, "access_token": token, "v": "5.103"}
    response = requests.get(url, params=params)
    return response.json()


def delete_from_friends(user_id):
    url = "<https://api.vk.com/method/friends.delete>"
    params = {"user_id": user_id, "access_token": token, "v": "5.103"}
    response = requests.get(url, params=params)
    return response.json()


def get_user_info(user_id):
    url = "<https://api.vk.com/method/users.get>"
    params = {
        "user_ids": user_id,
        "fields": "city, country, sex, bdate",
        "access_token": token,
        "v": "5.103",
    }
    response = requests.get(url, params=params)
    user_info = response.json()["response"][0]
    return user_info

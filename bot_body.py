import configparser
from random import randrange
import configparser

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


import bot_functions


config = configparser.ConfigParser()
config.read("token_list.ini")
token = config['VK']['bot_token']
user_id = config['VK']['user_id']

session = vk_api.VkApi(token=token)


def bot_body():
    bot_functions.greetings(session, user_id)
    while True:
        bot_functions.start_bot(session, user_id)
        gender = bot_functions.gender_choice(session, user_id)
        age_low = bot_functions.age_check_low(session, user_id)
        age_high = bot_functions.age_check_high(session, user_id, age_low)
        country = bot_functions.country_input(session, user_id)
        city = bot_functions.city_input(session, user_id)
        candidate_list = bot_functions.search_partner_list(session, user_id,
                                                        age_low, age_high,
                                                        gender, country, city)
        bot_functions.discuss_candidates(session, user_id, candidate_list)
        while True:
            decision = bot_functions.final_menu(session, user_id)
            if decision:
                bot_functions.discuss_candidates(session, user_id, candidate_list)
                continue
            else:
                break
        continue


if __name__ == '__main__':
    bot_body()

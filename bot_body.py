import configparser
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_functions

config = configparser.ConfigParser()
config.read("token_list.ini")
token = config.get("VK", "bot_token")
user_id = config.get("VK", "user_id")
session = vk_api.VkApi(token=token)


def bot_body(event):
    bot_functions.greetings(session, event, user_id)
    gender = bot_functions.gender_choice(session, event, user_id)
    age_low = bot_functions.age_check_low(session, event, user_id)
    age_high = bot_functions.age_check_high(session, event, user_id)
    country = bot_functions.country_input(session, event, user_id)
    city = bot_functions.city_input(session, event, user_id)
    candidate_list = bot_functions.search_partner_list(
        session, user_id, age_low, age_high, gender, country, city
    )
    bot_functions.discuss_candidates(session, user_id, candidate_list)

    while True:
        event = session.method("messages.getLongPollHistory", {
            "ts": VkLongPoll(session).api._last_ts,
            "pts": VkLongPoll(session).api._last_pts,
            "preview_length": 0,
            "count": 1
        })['messages']['items'][0]

        if event.type == VkEventType.MESSAGE_EVENT and event.to_me and event.text:
            event = vk_api.bot_longpoll.VkBotEventType(event.raw[1]['type'])
        elif event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            pass
        else:
            continue

        decision = bot_functions.final_menu(session, user_id, candidate_list, event)
        if not decision:
            break

        bot_functions.discuss_candidates(session, user_id, candidate_list)


if __name__ == "__main__":
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot_body(event)

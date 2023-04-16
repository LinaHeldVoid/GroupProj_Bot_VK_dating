from bot.functions import greetings
from vk.search_candidates import search_partner_list


def bot_body(session, user_id):
    greetings(session, user_id)
    while True:
        start_bot(session, user_id)
        gender = gender_choice(session, user_id)
        age_low = age_check_low(session, user_id)
        age_high = age_check_high(session, user_id, age_low)
        country = country_input(session, user_id)
        city = city_input(session, user_id)
        candidate_list = search_partner_list(
            session, user_id, age_low, age_high, gender, country, city
        )
        discuss_candidates(session, user_id, candidate_list)
        while True:
            decision = final_menu(session, user_id)
            if decision:
                discuss_candidates(session, user_id, candidate_list)
                continue
            else:
                break
        continue

        decision = final_menu(session, user_id, candidate_list, event)
        if not decision:
            break

        discuss_candidates(session, user_id, candidate_list)

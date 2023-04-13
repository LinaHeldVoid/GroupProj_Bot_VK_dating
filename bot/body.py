import bot.functions

def bot_body(event):
    functions.greetings(session, event, user_id)
    gender = functions.gender_choice(session, event, user_id)
    age_low = functions.age_check_low(session, user_id)
    age_high = functions.age_check_high(session, user_id)
    country = functions.country_input(session, user_id)
    city = functions.city_input(session, user_id)
    candidate_list = functions.search_partner_list(
        session, user_id, age_low, age_high, gender, country, city
    )
    functions.discuss_candidates(session, user_id, candidate_list)
    while True:
        decision = functions.final_menu(session, user_id, candidate_list)
        if decision:
            functions.discuss_candidates(session, user_id, candidate_list)
            continue

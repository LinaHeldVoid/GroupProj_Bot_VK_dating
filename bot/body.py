import asyncio
from bot.functions import *
from vk.search_candidates import search_partner_list


async def loop(session, user_id, age_low, age_high, gender):
    tasks = [
        discuss_candidates(session, user_id),
        search_partner_list(session, user_id, age_low, age_high, gender),
    ]
    await asyncio.gather(*tasks)


def bot_body(session, user_id):
    greetings(session, user_id)
    while True:
        start_bot(session, user_id)
        gender = gender_choice(session, user_id)
        age_low = age_check_low(session, user_id)
        age_high = age_check_high(session, user_id, age_low)
        asyncio.run(loop(session, user_id, age_low, age_high, gender))
        while True:
            decision = final_menu(session, user_id)
            if decision:
                asyncio.run(loop(session, user_id, age_low, age_high, gender))
                continue
            else:
                break
        continue

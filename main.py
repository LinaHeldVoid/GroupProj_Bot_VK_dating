from bot.body import bot_body
import vk_api
from data.token_list import bot_token, user_id
from db.db_functions import create_db


session = vk_api.VkApi(token=bot_token)

if __name__ == "__main__":
    bot_body(session, user_id)

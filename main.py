from bot.body import bot_body
import configparser
import vk_api

config = configparser.ConfigParser()
config.read("token_list.ini")
token = config.get("VK", "bot_token")
user_id = config.get("VK", "user_id")
session = vk_api.VkApi(token=token)

if __name__ == "__main__":
    bot_body(session, user_id)

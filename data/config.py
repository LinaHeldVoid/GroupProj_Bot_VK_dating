import configparser


def get_tokens():
    config = configparser.ConfigParser()
    config.read("token_list.py")
    token = config["VK"]["bot_token"]
    user_id = config["VK"]["user_id"]
    return token, user_id

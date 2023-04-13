import configparser

config = configparser.ConfigParser()
config.read("token_list.ini")
token = config["VK"]["bot_token"]
user_id = config["VK"]["user_id"]
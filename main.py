import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from bot.body import bot_body
from data.config import token

if __name__ == "__main__":
    session = vk_api.VkApi(token=token)
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot_body(event)

"""Module to get updates from telegram"""

import os

import httpx
from rich import print
from dotenv import load_dotenv
from wrapworks import cwdtoenv

load_dotenv()
cwdtoenv()


from src.models.telegram_update_models import TelegramUpdatePing


def get_updates():

    res = httpx.get(f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/getUpdates")
    print(res.text)


def send_message(update: TelegramUpdatePing, response: str):
    base_url = f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/sendMessage"

    # # TESTING
    # chat_id = -865047911
    # message = "Hello @KnotAsaniczka"
    # params = {
    #     "chat_id": chat_id,
    #     "text": message,
    # }
    params = {
        "chat_id": update.message.chat.id,
        "text": response,
        "reply_to_message_id": update.message.message_id,
    }
    res = httpx.post(base_url, params=params)

    print("Message sent")

    return TelegramUpdatePing(**res.json())


if __name__ == "__main__":
    send_message(1, 1)

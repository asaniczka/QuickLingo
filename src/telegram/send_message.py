"""Module to get updates from telegram"""

import os

import httpx
from rich import print


from src.models.update_models import TelegramUpdatePing


def get_updates():

    res = httpx.get(f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/getUpdates")
    print(res.text)


def send_message(update: TelegramUpdatePing, response: str):
    chat_id = -865047911
    message = "Hello @KnotAsaniczka"
    base_url = f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/sendMessage"

    params = {
        "chat_id": update.message.chat.id,
        "text": response,
        "reply_to_message_id": update.message.message_id,
    }
    res = httpx.post(base_url, params=params)

    print(res.text)
    print("Message sent")


if __name__ == "__main__":
    pass

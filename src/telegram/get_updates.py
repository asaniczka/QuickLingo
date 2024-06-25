"""Module to get updates from telegram"""

import os

import httpx
from rich import print


from src.models.update_models import TelegramUpdatePing


def set_webhook():

    domain = (
        "https://df5d-2402-4000-2200-f045-ca71-8f70-c463-d08b.ngrok-free.app/updates"
    )

    params = {"url": domain}
    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/setWebhook",
        params=params,
    )
    print(res.text)


def delete_webhook():

    domain = "ep_2iNzEveW0WCQrZDE4ITl7Fw64Ne"
    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/deleteWebhook"
    )
    print(res.text)


def get_updates():

    res = httpx.get(f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/getUpdates")
    print(res.text)


def send_message(update: TelegramUpdatePing, response: str):
    chat_id = -865047911
    message = "Hello @KnotAsaniczka"
    base_url = f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/sendMessage"

    params = {
        "chat_id": update.message.chat.id,
        "text": f"@{update.message.from_.username} {response}",
        "reply_to_message_id": update.message.message_id,
    }
    res = httpx.post(base_url, params=params)

    print(res.text)


if __name__ == "__main__":
    set_webhook()

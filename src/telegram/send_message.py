"""Module to get updates from telegram"""

import os

import httpx
from rich import print
from dotenv import load_dotenv
from wrapworks import cwdtoenv

load_dotenv()
cwdtoenv()


from src.models.telegram_update_models import (
    TelegramUpdatePing,
    TelegramUpdateNewMember,
)


def get_updates():

    res = httpx.get(f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/getUpdates")
    print(res.text)


def send_welcome_message(update: TelegramUpdateNewMember):
    base_url = f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/sendMessage"
    params = {
        "chat_id": update.message.chat.id,
        "text": f"👋 Hello @{update.message.new_chat_member.username or update.message.new_chat_member.first_name}, Welcome!! 🎉 I'm QuickLingoBot 🤖 and I'm here to help you learn English 📚. Tag me with @QuickLingoBot in a message to talk with me 💬",
    }
    res = httpx.post(base_url, params=params)
    print("Message sent")
    try:
        _ = TelegramUpdatePing(**res.json())
    except Exception as e:
        print(
            f"Error in parsing my reply: {type(e)}: {e}\n{res.status_code} - {res.text}"
        )

    return "Welcome message sent"


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
    formatted_response = None
    try:
        formatted_response = TelegramUpdatePing(**res.json())
    except Exception as e:
        print(f"Error in parsing my reply: {type(e)}: {e}")
        raise AttributeError(res.json()) from e

    return formatted_response


if __name__ == "__main__":
    send_message(1, 1)

"""
Main handler of messages
"""

# pylint:disable=wrong-import-position

from fastapi import FastAPI
import uvicorn
from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print

cwdtoenv()
load_dotenv()

from src.genai.generate_message import entry_generate_response_from_user_message
from src.telegram.send_message import send_message

from src.models.update_models import TelegramUpdatePing, ChatType


def entry_process_message(updates: TelegramUpdatePing) -> str:
    """"""

    if updates.message.chat.type in {ChatType.SUPERGROUP, ChatType.GROUP}:
        print(type(updates.message.chat.type))
        if "@quicklingo" not in updates.message.text.lower():
            return
    response = entry_generate_response_from_user_message(updates)
    send_message(updates, response)
    return response

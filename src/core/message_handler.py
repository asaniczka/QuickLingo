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
from src.postgres.insert_functions import insert_user, insert_chat, insert_message
from src.postgres.select_functions import check_if_chat_is_authorized

from src.models.telegram_update_models import TelegramUpdatePing, ChatType
from src.models.gen_ai_models import LLMRoles


def record_message_in_db(updates: TelegramUpdatePing):
    """"""

    insert_user(updates.message.from_)
    insert_chat(updates.message.chat)
    insert_message(updates.message, LLMRoles.USER)


def entry_process_message(updates: TelegramUpdatePing) -> str:
    """"""
    is_authorized = check_if_chat_is_authorized(updates.message.chat.id)

    if not is_authorized:
        send_message(updates, "Sorry, You need a paid subscription for this")
        return "Chat Not Authorized"

    if updates.message.chat.type in {ChatType.SUPERGROUP, ChatType.GROUP}:
        print(type(updates.message.chat.type))
        if "@quicklingo" not in updates.message.text.lower():
            return "Group message was not tagged"

    response = entry_generate_response_from_user_message(updates)
    send_message(updates, response)

    record_message_in_db(updates)
    return response

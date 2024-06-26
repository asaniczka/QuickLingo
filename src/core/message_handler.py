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


def record_message_in_db(
    updates: TelegramUpdatePing,
    role: LLMRoles = LLMRoles.USER,
    cost=0,
    input_tokens=0,
    output_tokens=0,
):
    """"""

    insert_user(updates.message.from_)
    insert_chat(updates.message.chat)
    insert_message(
        updates.message,
        role,
        cost,
        input_tokens,
        output_tokens,
    )


def entry_process_message(updates: TelegramUpdatePing) -> str:
    """"""
    is_authorized = check_if_chat_is_authorized(updates.message.chat.id)

    if not is_authorized:
        send_message(
            updates,
            "Sorry, You need a paid subscription to Sona.EnglishClub to use QuickLingoBot. Please contact @Sona_mhmdi",
        )
        record_message_in_db(updates)
        return "Chat Not Authorized"

    if updates.message.chat.type in {ChatType.SUPERGROUP, ChatType.GROUP}:
        if "@quicklingo" not in updates.message.text.lower():
            record_message_in_db(updates)
            return "Group message was not tagged"

    response = entry_generate_response_from_user_message(updates)
    reply_data = send_message(updates, response.text)

    record_message_in_db(
        updates,
        cost=response.cost,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
    )
    record_message_in_db(
        reply_data,
        role=LLMRoles.AI,
    )
    return response

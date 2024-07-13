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
from src.postgres.select_functions import (
    check_if_chat_is_authorized,
    check_if_user_has_credits,
)

from src.models.telegram_update_models import TelegramUpdatePing, ChatType
from src.models.gen_ai_models import LLMRoles


def record_message_in_db(
    updates: TelegramUpdatePing,
    role: LLMRoles = LLMRoles.USER,
    cost=0,
    input_tokens=0,
    output_tokens=0,
    was_tagged=False,
):
    """"""

    insert_user(updates.message.from_)
    insert_chat(updates.message.chat)
    insert_message(updates.message, role, cost, input_tokens, output_tokens, was_tagged)


def entry_process_message(update: TelegramUpdatePing) -> str:
    """"""
    is_authorized = check_if_chat_is_authorized(update.message.chat.id)
    if not is_authorized:
        send_message(
            update,
            """دوست عزیز، برای استفاده از چت شخصی با ربات شما نیاز به پرداخت حق عضویت دارید. برای اطلاعات بیشتر به این آیدی پیام بدین
@NaturalEnglish_Admin""",
        )
        record_message_in_db(update)
        return "Chat Not Authorized"

    if update.message.chat.type in {ChatType.SUPERGROUP, ChatType.GROUP}:
        if "#noreply" not in update.message.text.lower():
            record_message_in_db(update)
            return "Ignore message command found"

    has_usage = check_if_user_has_credits(
        update.message.chat.id, update.message.from_.id
    )
    if not has_usage:
        send_message(
            update,
            f"⚠️ Sorry @{update.message.from_.username or update.message.from_.first_name}, you've used all your credits for today⏳ Please wait till tomorrow to try agian 🌞",
        )
        record_message_in_db(update)
        return "User doesn't have credits"

    response = entry_generate_response_from_user_message(update)
    reply_data = send_message(update, response.text)

    record_message_in_db(
        update,
        cost=response.cost,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        was_tagged=True,
    )
    record_message_in_db(
        reply_data,
        role=LLMRoles.AI,
    )
    return response

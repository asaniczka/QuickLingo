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
from src.models.gen_ai_models import LLMRoles, AIResponse


def record_message_in_db(
    updates: TelegramUpdatePing,
    role: LLMRoles = LLMRoles.USER,
    cost=0,
    input_tokens=0,
    output_tokens=0,
    was_tagged=False,
):
    """
    ### Responsibility:
        - Record a message and its associated details into the database.
        - Insert user and chat information into the database if they do not already exist.

    ### Args:
        - `updates`: TelegramUpdatePing
            An object containing update information including user, chat, and message details.
        - `role`: LLMRoles, optional
            The role of the message sender, default is `LLMRoles.USER`.
        - `cost`: int, optional
            The cost associated with processing the message, default is 0.
        - `input_tokens`: int, optional
            The number of input tokens used, default is 0.
        - `output_tokens`: int, optional
            The number of output tokens generated, default is 0.
        - `was_tagged`: bool, optional
            Whether the message was tagged, default is False.

    ### Returns:
        - None

    ### How does the function work:
        - Inserts user information into the database using `insert_user`.
        - Inserts chat information into the database using `insert_chat`.
        - Inserts the message and its associated details into the database using `insert_message`.
    """

    insert_user(updates.message.from_)
    insert_chat(updates.message.chat)
    insert_message(updates.message, role, cost, input_tokens, output_tokens, was_tagged)


def entry_process_message(update: TelegramUpdatePing) -> AIResponse:
    """
    ### Responsibility:
        - Process a Telegram message update and generate a response if the chat and user are authorized and have credits.
        - Handle unauthorized chat, specific commands, and user credits checks before generating a response.

    ### Args:
        - `update`: TelegramUpdatePing
            An object containing update information including chat, user, and message details.

    ### Returns:
        - `response`: AIResponse or str
            Returns an `AIResponse` object if the message is processed and a response is generated.
            Returns a string with a message indicating the result if the chat is not authorized, an ignore command is found, or the user doesn't have credits.

    ### How does the function work:
        - Checks if the chat is authorized using `check_if_chat_is_authorized`. If not, sends an authorization message and records the message in the database.
        - Checks if the chat type is a SUPERGROUP or GROUP and if the text contains the "#noreply" command. If found, records the message in the database and returns.
        - Checks if the user has credits using `check_if_user_has_credits`. If not, sends a message indicating the usage limit and records the message in the database.
        - Calls `entry_generate_response_from_user_message` to generate a response if all checks pass.
        - Sends the generated response message.
        - Records both the user's message and the generated response in the database with their associated details.
    """
    
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
        if "#noreply" in update.message.text.lower():
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

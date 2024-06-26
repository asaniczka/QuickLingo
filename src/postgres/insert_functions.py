"""
Functions to insert into postgres
"""

from psycopg.errors import UniqueViolation

from src.models.telegram_update_models import TelegramUser, TelegramChat, Message
from src.postgres.core_db_operations import POSTGRES_POOL
from src.models.gen_ai_models import LLMRoles


def insert_user(user: TelegramUser):
    """"""

    statement = """
    INSERT INTO USERS (USER_ID,FIRST_NAME,LAST_NAME,USERNAME,IS_BOT)
    VALUES (%s,%s,%s,%s,%s)
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    statement,
                    (
                        user.id,
                        user.first_name,
                        user.last_name,
                        user.username,
                        user.is_bot,
                    ),
                )
            except UniqueViolation:
                return


def insert_chat(chat: TelegramChat):
    """"""

    statement = """
    INSERT INTO CHATS (CHAT_ID,TITLE,TYPE)
    VALUES (%s,%s,%s)
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    statement,
                    (chat.id, chat.title, chat.type),
                )
            except UniqueViolation:
                return


def insert_message(
    message: Message, role: LLMRoles, cost=0, input_token=0, output_tokens=0
):
    """"""

    statement = """
    INSERT INTO MESSAGES (
        MESSAGE_ID,
        ROLE,
        USER_ID,
        CHAT_ID,
        MESSAGE,
        COST,
        INPUT_TOKENS,
        OUTPUT_TOKENS)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    statement,
                    (
                        message.message_id,
                        role.value,
                        message.from_.id,
                        message.chat.id,
                        message.text,
                        cost,
                        input_token,
                        output_tokens,
                    ),
                )
            except UniqueViolation:
                return

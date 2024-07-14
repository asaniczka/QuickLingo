"""
Functions to insert into postgres
"""

from psycopg.errors import UniqueViolation

from src.models.telegram_update_models import TelegramUser, TelegramChat, Message
from src.postgres.core_db_operations import POSTGRES_POOL
from src.models.gen_ai_models import LLMRoles


def insert_user(user: TelegramUser):
    """
    ### Responsibility:
        - Insert a new Telegram user into the database.
        - Handle any uniqueness conflict by ignoring duplicate entries.

    ### Args:
        - `user`: TelegramUser
            An object containing user details such as ID, first name, last name, username, and bot status.

    ### Returns:
        - None

    ### How does the function work:
        - Defines a SQL query that:
            - Inserts the user's ID, first name, last name, username, and bot status into the `USERS` table.
            - Ignores the insertion if a user with the same ID already exists (ON CONFLICT DO NOTHING).
        - Executes the SQL query using a connection from the `POSTGRES_POOL`.
        - Catches any `UniqueViolation` exceptions to handle conflicts.
        - Returns None if an exception occurs.
    """

    statement = """
    INSERT INTO USERS (USER_ID,FIRST_NAME,LAST_NAME,USERNAME,IS_BOT)
    VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT (USER_ID) DO NOTHING;
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
    """
    ### Responsibility:
        - Insert a new Telegram chat into the database.
        - Handle any uniqueness conflict by ignoring duplicate entries.

    ### Args:
        - `chat`: TelegramChat
            An object containing chat details such as ID, title, and type.

    ### Returns:
        - None

    ### How does the function work:
        - Defines a SQL query that:
            - Inserts the chat's ID, title, and type into the `CHATS` table.
            - Ignores the insertion if a chat with the same ID already exists (ON CONFLICT DO NOTHING).
        - Executes the SQL query using a connection from the `POSTGRES_POOL`.
        - Catches any `UniqueViolation` exceptions to handle conflicts.
        - Returns None if an exception occurs.
    """

    statement = """
    INSERT INTO CHATS (CHAT_ID,TITLE,TYPE)
    VALUES (%s,%s,%s)
    ON CONFLICT (CHAT_ID) DO NOTHING;
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
    message: Message,
    role: LLMRoles,
    cost=0,
    input_token=0,
    output_tokens=0,
    was_tagged: bool = False,
):
    """
    ### Responsibility:
        - Insert a new message into the database with associated metadata such as role, cost, and token counts.
        - Handle any uniqueness conflict by ignoring duplicate entries.

    ### Args:
        - `message`: Message
            An object containing message details such as ID, text, sender, and chat.
        - `role`: LLMRoles
            The role associated with the message (e.g., user, assistant).
        - `cost`: float, optional (default is 0)
            The cost associated with the message.
        - `input_token`: int, optional (default is 0)
            The number of input tokens for the message.
        - `output_tokens`: int, optional (default is 0)
            The number of output tokens for the message.
        - `was_tagged`: bool, optional (default is False)
            Indicates whether the message was tagged.

    ### Returns:
        - None

    ### How does the function work:
        - Defines a SQL query that:
            - Inserts message details including the message ID, role, user ID, chat ID, message content, cost, input tokens, output tokens, and tagged status into the `MESSAGES` table.
        - Executes the SQL query using a connection from the `POSTGRES_POOL`.
        - Catches any `UniqueViolation` exceptions to handle conflicts.
        - Returns None if an exception occurs.
    """

    statement = """
    INSERT INTO MESSAGES (
        MESSAGE_ID,
        ROLE,
        USER_ID,
        CHAT_ID,
        MESSAGE,
        COST,
        INPUT_TOKENS,
        OUTPUT_TOKENS,
        WAS_TAGGED)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
                        was_tagged,
                    ),
                )
            except UniqueViolation:
                return

"""Functions that select from postgres"""

from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print

cwdtoenv()
load_dotenv()

from src.postgres.core_db_operations import POSTGRES_POOL
from src.models.postgres_models import Message


def check_if_chat_is_authorized(chat_id: int) -> bool:
    """
    ### Responsibility:
        - Check if a given chat is authorized by querying a database.
        - Return the authorization status.

    ### Args:
        - `chat_id`: int
            The ID of the chat to be checked for authorization.

    ### Returns:
        - `is_authorized`: bool
            True if the chat is authorized, False otherwise.

    ### How does the function work:
        - Defines an SQL query to select the authorization status from the `CHATS` table using the given `chat_id`.
        - Executes the SQL query using a connection from the `POSTGRES_POOL`.
        - Fetches the first result and prints the retrieved data.
        - Returns True if the chat is authorized; otherwise, returns False.
    """

    statement = """
    SELECT 
        IS_AUTHORIZED 
    FROM 
        PUBLIC.CHATS
    WHERE 
        chat_id = %s
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (chat_id,))
            data = cur.fetchone()
            print(f"check_if_chat_is_authorized: {data}")
            return bool(data[0] if data else 0)


def check_if_user_has_credits(chat_id: int, user_id: int) -> bool:
    """
    ### Responsibility:
        - Check if a user in a given chat has available message credits for the current day.
        - Return the credit availability status.

    ### Args:
        - `chat_id`: int
            The ID of the chat where the user belongs.
        - `user_id`: int
            The ID of the user whose credits are being checked.

    ### Returns:
        - `has_credits`: bool
            True if the user has remaining credits for the day; otherwise, False.

    ### How does the function work:
        - Defines a SQL query that:
            - Computes the number of messages the user has tagged today in the chat (`USAGE`).
            - Retrieves the allowed usage per day for the chat from the `CHATS` table (`ALLOWED`).
            - Calculates the remaining credits by subtracting the usage count from the allowed usage.
        - Executes the SQL query using a connection from the `POSTGRES_POOL`.
        - Fetches the result which indicates the remaining credits.
        - Prints the retrieved data.
        - Returns True if the user has more than 0 remaining credits; otherwise, returns False.
    """

    statement = """
    WITH
        USAGE AS (
            SELECT
                COUNT(1)
            FROM
                PUBLIC.MESSAGES
            WHERE
                CHAT_ID = %s
                AND USER_ID = %s
                AND DATE (INSERTED_DATE) = CURRENT_DATE
                AND WAS_TAGGED = TRUE
        ),
        ALLOWED AS (
            SELECT
                ALLOWED_USAGE_PER_DAY
            FROM
                PUBLIC.CHATS
            WHERE
                CHAT_ID = %s
        )
    SELECT
        ALLOWED.ALLOWED_USAGE_PER_DAY - USAGE.COUNT
    FROM
        USAGE,
        ALLOWED;
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (chat_id, user_id, chat_id))
            data = cur.fetchone()
            print(f"check_if_user_has_credits: {data}")
            return bool(data[0] > 0)


def get_last_n_messages(chat_id: int, user_id: str, n=5) -> list[Message]:
    """
    ### Responsibility:
        - Retrieve the last `n` messages for a specified user in a given chat.
        - Return the messages as a list of `Message` objects.

    ### Args:
        - `chat_id`: int
            The ID of the chat to retrieve messages from.
        - `user_id`: str
            The ID of the user whose messages are being retrieved.
        - `n`: int, optional (default is 5)
            The number of most recent messages to retrieve.

    ### Returns:
        - `messages`: list[Message]
            A list of `Message` objects containing the last `n` messages sorted by message ID in ascending order.

    ### How does the function work:
        - Defines a SQL query that:
            - Selects the message ID, message content, and role from the `messages` table for the given `chat_id` and `user_id`.
            - Orders the results by message ID in descending order and limits the number of results to `n`.
        - Executes the SQL query using a connection from the `POSTGRES_POOL`.
        - Fetches all resulting rows.
        - Creates `Message` objects for each row and stores them in a list.
        - Sorts the messages list by message ID in ascending order.
        - Returns the sorted list of `Message` objects.
    """

    statement = """
    SELECT PG_MESSAGE_ID,MESSAGE,ROLE
    FROM messages
    WHERE chat_id = %s
    ORDER BY PG_MESSAGE_ID DESC
    LIMIT %s;
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (chat_id, n))
            data = cur.fetchall()

    messages = [Message(pg_message_id=x[0], message=x[1], role=x[2]) for x in data]
    messages.sort(key=lambda x: x.pg_message_id)
    return messages


if __name__ == "__main__":
    messages = get_last_n_messages(-1002248772367, 5159937523)
    print(messages)

"""Functions that select from postgres"""

from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print

cwdtoenv()
load_dotenv()

from src.postgres.core_db_operations import POSTGRES_POOL
from src.models.postgres_models import Message


def check_if_chat_is_authorized(chat_id: int):
    """"""

    statement = """
    SELECT IS_AUTHORIZED FROM CHATS
    WHERE chat_id = %s
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (chat_id,))
            data = cur.fetchone()
            print(data)
            return bool(data[0] if data else 0)


def get_last_n_messages(chat_id: int, n=10) -> list[Message]:
    """"""

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
    messages = get_last_n_messages(-4184813078)
    print(messages)

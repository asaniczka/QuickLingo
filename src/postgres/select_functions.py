"""Functions that select from postgres"""

from src.postgres.core_db_operations import POSTGRES_POOL


def check_if_chat_is_authorized(chat_id: int):
    """"""

    statement = """
    SELECT IS_AUTHORIZED FROM CHATS
    WHERE chat_id = %s
    """

    with POSTGRES_POOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (chat_id,))
            data = cur.fetchone
            return bool(data[0])

"""
Celery workers
"""

# pylint:disable=wrong-import-position

import os

from celery import Celery
from wrapworks import cwdtoenv
from dotenv import load_dotenv

cwdtoenv()
load_dotenv()

from src.core.message_handler import entry_process_message
from src.telegram.send_message import send_welcome_message
from src.models.telegram_update_models import (
    TelegramUpdatePing,
    TelegramUpdateNewMember,
)


celery_master = Celery(
    broker=os.getenv("CELERY_BROKER"), backend=os.getenv("CELERY_BACKEND")
)
celery_master.config_from_object(
    {
        "event_serializer": "json",
        "task_serializer": "pickle",
        "result_serializer": "pickle",
        "accept_content": ["application/json", "application/x-python-serialize"],
        "broker_connection_retry_on_startup": True,
    }
)


@celery_master.task(bind=True, name="handle_update")
def worker_handle_update(self, update: TelegramUpdatePing | TelegramUpdateNewMember):
    """
    ### Responsibility:
        - Handle different types of Telegram updates and dispatch them to the appropriate handler functions.

    ### Args:
        - `update`: TelegramUpdatePing | TelegramUpdateNewMember
            An object representing either a message update or a new member update.

    ### Returns:
        - `result`: AIResponse or str or None
            Returns the result of processing the update using the appropriate handler function.
                - For `TelegramUpdatePing`, it returns the result from `entry_process_message`.
                - For `TelegramUpdateNewMember`, it returns the result from `send_welcome_message`.

    ### Raises:
        - `AttributeError`:
            Raised if the provided update type is not recognized or supported.

    ### How does the function work:
        - Checks if the update is of type `TelegramUpdatePing`. If so, calls `entry_process_message` and returns the result.
        - Checks if the update is of type `TelegramUpdateNewMember`. If so, calls `send_welcome_message` and returns the result.
        - Raises an `AttributeError` if the update type is unrecognized.
    """

    if isinstance(update, TelegramUpdatePing):
        result = entry_process_message(update)
        return result
    if isinstance(update, TelegramUpdateNewMember):
        result = send_welcome_message(update)
        return result
    else:
        raise AttributeError(f"Unknown update type: {type(update).__name__}: {update}")

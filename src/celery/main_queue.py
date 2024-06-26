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
from src.models.telegram_update_models import TelegramUpdatePing


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
def worker_handle_update(self, updates: TelegramUpdatePing):
    """"""

    result = entry_process_message(updates)
    return result

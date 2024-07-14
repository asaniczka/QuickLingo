"""Main ingestion API"""

# pylint:disable=wrong-import-position

from typing import Any

from fastapi import FastAPI
import uvicorn
from rich import print
from wrapworks import cwdtoenv
from dotenv import load_dotenv

cwdtoenv()
load_dotenv()

from src.genai.generate_message import entry_generate_response_from_user_message
from src.telegram.send_message import send_message
from src.celery.main_queue import worker_handle_update
from src.models.telegram_update_models import (
    TelegramUpdatePing,
    TelegramUpdateNewMember,
)


app = FastAPI()


@app.get("/")
def health_check():
    return "I'm running smoothly"


@app.post("/updates")
def listen_for_updates(update: dict):
    """
    ### Description:
    - Handles incoming updates from Telegram.
    - Determines the type of update and processes it accordingly.

    ### Args:
    - `update`: Dictionary containing the update payload from Telegram.
      - Keys may include "message", "text", "new_chat_member", etc.
    """

    try:
        if "text" in update["message"]:
            update: TelegramUpdatePing = TelegramUpdatePing(**update)
        elif "new_chat_member" in update["message"]:
            update: TelegramUpdateNewMember = TelegramUpdateNewMember(**update)
    except Exception as e:
        print(f"Couldn't parse what telegram sent:\n{update}")
        print(f"{type(e).__name__}: {e}")
        return

    _ = worker_handle_update.delay(update)
    return


if __name__ == "__main__":
    uvicorn.run(app=app, port=9090)

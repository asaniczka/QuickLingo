"""Main ingestion API"""

from fastapi import FastAPI
import uvicorn
from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print

cwdtoenv()
load_dotenv()

from src.genai.generate_message import entry_generate_response_from_user_message
from src.telegram.get_updates import send_message

from src.models.update_models import TelegramUpdatePing


app = FastAPI()


@app.post("/updates")
def listen_for_updates(updates: TelegramUpdatePing):
    print(updates)
    response = entry_generate_response_from_user_message(updates)
    send_message(updates, response)


if __name__ == "__main__":
    uvicorn.run(app=app, port=9090)

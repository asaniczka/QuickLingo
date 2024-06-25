"""Module to get updates from telegram"""

import os

import httpx
from rich import print
from pydantic import BaseModel, ConfigDict, Field


class FromWho(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str


class TelegramChat(BaseModel):
    id: int
    title: str
    type: str
    all_members_are_administrators: bool


class Message(BaseModel):
    message_id: int
    from_: FromWho = Field(alias="from")
    chat: TelegramChat
    date: int
    text: str


class TelegramUpdateResult(BaseModel):
    update_id: int
    message: Message


class APIResponse(BaseModel):
    ok: bool
    result: list[TelegramUpdateResult]


def get_updates():

    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv("TELBOTKEY")}/getUpdates")
    print(res.text)


def send_message():
    chat_id = -865047911
    message = "Hello @KnotAsaniczka"
    base_url = f"https://api.telegram.org/bot{os.getenv("TELBOTKEY")}/sendMessage"

    params = {"chat_id": chat_id, "text": message,
              "ReplyParameters": {"message_id": 4, "chat_id": chat_id,}}

    res = httpx.post(base_url, params=params)

    print(res.text)


if __name__ == "__main__":
    send_message()

from pydantic import BaseModel
from datetime import datetime


class TelegramUser(BaseModel):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    is_bot: bool = False
    last_active: datetime


class Chat(BaseModel):
    chat_id: int
    title: str
    type: str
    is_authorized: bool = False
    last_active: datetime


class Message(BaseModel):
    pg_message_id: int | None = None
    message_id: int | None = None
    role: str | None = None
    user_id: int | None = None
    chat_id: int | None = None
    message: str | None = None
    cost: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    inserted_date: datetime | None = None

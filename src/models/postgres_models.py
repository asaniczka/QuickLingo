from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    is_bot: bool = False


class Chat(BaseModel):
    chat_id: int
    title: str
    type: str
    is_authorized: bool = False


class Message(BaseModel):
    pg_message_id: int | None = None
    message_id: int
    role: str
    user_id: int
    chat_id: int
    message: str
    cost: float = None
    input_tokens: int = None
    output_tokens: int = None
    inserted_date: datetime | None = None

from pydantic import BaseModel, ConfigDict, Field


class FromWho(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None


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


class TelegramUpdatePing(BaseModel):
    update_id: int
    message: Message

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, AliasChoices, AliasPath


class ChatType(Enum):
    GROUP = "group"
    SUPERGROUP = "supergroup"
    PRIVATE = "private"


class FromWho(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None


class TelegramChat(BaseModel):
    id: int
    title: str = Field(
        validation_alias=AliasChoices(AliasPath("title"), AliasPath("username"))
    )
    type: ChatType
    all_members_are_administrators: bool = False


class Message(BaseModel):
    message_id: int
    from_: FromWho = Field(alias="from")
    chat: TelegramChat
    date: int
    text: str


class TelegramUpdatePing(BaseModel):
    update_id: int
    message: Message

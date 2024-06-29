from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, AliasChoices, AliasPath


class ChatType(Enum):
    GROUP = "group"
    SUPERGROUP = "supergroup"
    PRIVATE = "private"


class TelegramUser(BaseModel):
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
    from_: TelegramUser = Field(validation_alias=AliasPath("from"))
    chat: TelegramChat
    date: int
    text: str


class TelegramUpdatePing(BaseModel):
    update_id: int | None = None
    message: Message = Field(
        validation_alias=AliasChoices(AliasPath("message"), AliasPath("result"))
    )


class NewMemberData(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str | None = None
    language_code: str | None = None


class NewMemberWrapper(BaseModel):
    new_chat_member: NewMemberData
    from_: TelegramUser = Field(validation_alias=AliasPath("from"))
    chat: TelegramChat
    date: int


class TelegramUpdateNewMember(BaseModel):
    update_id: int | None = None
    message: NewMemberWrapper

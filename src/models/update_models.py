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


class TelegramUpdatePing(BaseModel):
    update_id: int
    message: Message


{
    "update_id": 606293319,
    "message": {
        "message_id": 10,
        "from": {
            "id": 1892096500,
            "is_bot": False,
            "first_name": "Asaniczka",
            "last_name": ":)",
            "username": "KnotAsaniczka",
        },
        "chat": {
            "id": -865047911,
            "title": "MyBotRun Notifications",
            "type": "group",
            "all_members_are_administrators": True,
        },
        "date": 1719347412,
        "text": "Noo",
    },
}

CREATE INDEX IF NOT EXISTS idx_messages_chatid_pgmessageid ON messages(chat_id, PG_MESSAGE_ID);

CREATE INDEX IF NOT EXISTS idx_messages_chatid_userid_wastagged_date ON messages(CHAT_ID, USER_ID, INSERTED_DATE, WAS_TAGGED);

CREATE INDEX IF NOT EXISTS idx_chats_chatid ON CHATS(CHAT_ID);

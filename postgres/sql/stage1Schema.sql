--
-- Create the USERS table if it doesn't exist
--
CREATE TABLE IF NOT EXISTS
	USERS (
		USER_ID NUMERIC PRIMARY KEY,
		FIRST_NAME TEXT,
		LAST_NAME TEXT,
		USERNAME TEXT,
		IS_BOT BOOLEAN DEFAULT FALSE,
		LAST_ACTIVE TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);

--
-- Create the CHATS table if it doesn't exist
--
CREATE TABLE IF NOT EXISTS
	CHATS (
		CHAT_ID NUMERIC PRIMARY KEY,
		TITLE TEXT,
		TYPE TEXT,
		IS_AUTHORIZED BOOLEAN DEFAULT FALSE,
		LAST_ACTIVE TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);

--
-- Create the MESSAGES table if it doesn't exist
--
CREATE TABLE IF NOT EXISTS
	MESSAGES (
		PG_MESSAGE_ID BIGSERIAL PRIMARY KEY,
		MESSAGE_ID NUMERIC,
		ROLE TEXT NOT NULL,
		USER_ID NUMERIC NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
		CHAT_ID NUMERIC NOT NULL REFERENCES CHATS (CHAT_ID) ON DELETE CASCADE ON UPDATE CASCADE,
		MESSAGE TEXT NOT NULL,
		COST NUMERIC DEFAULT NULL::INT,
		INPUT_TOKENS NUMERIC DEFAULT NULL::INT,
		OUTPUT_TOKENS NUMERIC DEFAULT NULL::INT,
		INSERTED_DATE TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);

--
-- Function to update the LAST_ACTIVE timestamp in USERS and CHATS tables
--
CREATE
OR REPLACE FUNCTION UPDATE_LAST_ACTIVE () RETURNS TRIGGER AS $$
BEGIN

	UPDATE USERS
	SET LAST_ACTIVE = CURRENT_TIMESTAMP
	WHERE USERS.USER_ID = NEW.USER_ID;

	UPDATE CHATS
	SET LAST_ACTIVE = CURRENT_TIMESTAMP
	WHERE CHATS.CHAT_ID = NEW.CHAT_ID;

	RETURN NEW;

END;
$$ LANGUAGE PLPGSQL;

--
-- Create a trigger to update last active for USERS and CHATS after inserting a message
--
DROP TRIGGER IF EXISTS MESSAGES_UPDATE_LAST_ACTIVE_OF_PARENTS ON MESSAGES;

CREATE TRIGGER MESSAGES_UPDATE_LAST_ACTIVE_OF_PARENTS
AFTER INSERT ON MESSAGES FOR EACH ROW
EXECUTE FUNCTION UPDATE_LAST_ACTIVE ();

--
-- Alter CHATS table to add a new column ALLOWED_USAGE_PER_DAY
--
ALTER TABLE CHATS
ADD COLUMN ALLOWED_USAGE_PER_DAY NUMERIC DEFAULT 0;

--
-- Alter MESSAGES table to add a new column WAS_TAGGED
--
ALTER TABLE MESSAGES
ADD COLUMN WAS_TAGGED BOOLEAN DEFAULT FALSE;
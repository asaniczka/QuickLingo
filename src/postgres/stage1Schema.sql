CREATE TABLE IF NOT EXISTS
    messages (
        message_id SERIAL PRIMARY KEY,
        ROLE TEXT NOT NULL,
        user_id TEXT NOT NULL,
        message TEXT NOT NULL,
        COST NUMERIC DEFAULT NULL::INT
    );

CREATE TABLE IF NOT EXISTS
    users (
        user_id SERIAL PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        
    );
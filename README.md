# QuickLingoBot

QuickLingoBot is a Telegram bot that leverages Artificial Intelligence to provide automated responses to users' questions. 

This bot is specifically designed to help Persian speakers learn English.

QuickLingoBot can handle messages, interact with an AI service for generating responses, and manage user credits and authorizations.

## Features

- **Language Learning Assistance**: Specially designed to assist Persian speakers in learning English through interactive conversations and translations.
- **AI-Powered Responses**: Uses an AI service to process and generate responses based on user messages.
- **User and Chat Management**: Manages user and chat data, including message history and credits.
- **Authorization**: Checks if a chat is authorized to use the bot's services.
- **Credit System**: Ensures that users have available credits to ask questions.

## Getting Started

### Prerequisites

To set up and run QuickLingoBot, you'll need:

- Python 3.12
- A PostgreSQL database

### Installation

1. Clone the repository:
2. Create a virtual environment and activate it
3. Install the required packages using the `requirements.txt`
4. Set up environment variables following the `example.env`
5. Initialize a postgres DB using the schema in the `postgres` folder

### Running the Bot

Start the FastAPI server using uvicorn:

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

This will launch the FastAPI server which will start listening for incoming messages.

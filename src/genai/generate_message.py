"""
Issue requests to LLM using dynamic prompts
"""

# pylint:disable=wrong-import-position

from enum import Enum
import os
from datetime import datetime
import json
import re

import httpx
from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print


cwdtoenv()
load_dotenv()

from src.postgres.select_functions import get_last_n_messages
from src.models.gen_ai_models import (
    ValidLLMModels,
    LLM_COST_PER_TOKEN,
    LLMMessage,
    LLMMessageLog,
    AIResponse,
    LLMRoles,
)
from src.models.telegram_update_models import TelegramUpdatePing


def invoke_openai(model: ValidLLMModels | str, messages: LLMMessageLog) -> AIResponse:
    """
    ### Responsibility:
        - Invoke the OpenAI API with a specific model and message log to get a response.
        - Handle and raise any errors that occur during the API call or response parsing.

    ### Args:
        - `model`: ValidLLMModels | str
            The language model to use for the API call. Could be an instance of `ValidLLMModels` or a string.
        - `messages`: LLMMessageLog
            A log of messages (as instances of `LLMMessage`) to send to the API.

    ### Returns:
        - `response`: AIResponse
            The response from the OpenAI API parsed into an `AIResponse` object.

    ### Raises:
        - `RuntimeError`:
            Raised if the API response contains an error.
        - `Exception`:
            Raised if there is an error parsing the API response.

    ### How does the function work:
        - Converts `model` to its string representation if it is an instance of `ValidLLMModels`.
        - Constructs the payload for the OpenAI API call with the specified model and messages.
        - Sets the appropriate headers, including the API key from environment variables.
        - Sends a POST request to the OpenAI API endpoint.
        - Tries to parse the JSON response:
            - If it contains an error, prints the payload and raises a `RuntimeError`.
            - Returns an `AIResponse` object if parsing succeeds.
            - Catches and prints exceptions that occur during response parsing and raises the exception.
    """

    if not isinstance(model, str):
        model = model.value

    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [x.model_dump() for x in messages.messages],
        "max_tokens": 1500,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('AZ_OPENAI_API_KEY')}",
    }

    response = httpx.post(url, json=payload, headers=headers, timeout=120)

    try:
        data = response.json()
        if data.get("error"):
            print(payload)
            raise RuntimeError(data["error"]["message"])
        return AIResponse(**data)
    except RuntimeError:
        raise
    except Exception as e:
        print(f"Error parsing {response.text}: {type(e).__name__}: {e}")
        raise


def handler_generate_response(
    messages: LLMMessageLog, model: ValidLLMModels
) -> AIResponse:
    """
    ### Responsibility:
        - Generate a response from the OpenAI API using given messages and model.
        - Calculate the cost of the generated response based on the model's token cost.

    ### Args:
        - `messages`: LLMMessageLog
            A log of messages (as instances of `LLMMessage`) to send to the API.
        - `model`: ValidLLMModels
            The language model to use for generating the response.

    ### Returns:
        - `response`: AIResponse
            The response from the OpenAI API, with the cost calculated.

    ### How does the function work:
        - Calls the `invoke_openai` function to get a response from the API.
        - Calculates the cost of the response using the model's value and a predefined token cost (`LLM_COST_PER_TOKEN`).
        - Returns the `AIResponse` with the calculated cost.
    """

    response = invoke_openai(model, messages)
    response.calculate_cost(model.value, LLM_COST_PER_TOKEN)

    return response


def remove_handles_from_message(message: str) -> str:
    """
    ### Responsibility:
        - Remove any handles (e.g., @username) from a given message string.

    ### Args:
        - `message`: str
            The input message string from which handles need to be removed.

    ### Returns:
        - `message`: str
            The message string with all handles removed.

    ### How does the function work:
        - Compiles a regular expression pattern to match handles (e.g., @username).
        - Uses `re.sub` to replace any occurrences of the pattern in the message with an empty string.
        - Returns the cleaned message.
    """

    pattern = re.compile(r"(@\w+)")

    message = re.sub(pattern, "", message)
    return message


def format_telegram_chat_history(update: TelegramUpdatePing) -> list[LLMMessage]:
    """
    ### Responsibility:
        - Format the last N messages from a Telegram chat history into a list of `LLMMessage` objects.

    ### Args:
        - `update`: TelegramUpdatePing
            An object containing update information including chat ID and user ID.

    ### Returns:
        - `messages`: list[LLMMessage]
            A list of formatted `LLMMessage` objects containing the role and content of the last N messages.

    ### How does the function work:
        - Retrieves the last 5 messages from the chat using the `get_last_n_messages` function.
        - Converts each retrieved message into an `LLMMessage` object by mapping the message role and content.
        - Returns the list of `LLMMessage` objects.
    """

    messages = get_last_n_messages(update.message.chat.id, update.message.from_.id, n=3)

    return [LLMMessage(role=x.role, content=x.message) for x in messages]


def entry_generate_response_from_user_message(update: TelegramUpdatePing) -> AIResponse:
    """
    ### Responsibility:
        - Generate a response from the language model for a given user message received via a Telegram update.
        - Include both English and Persian translations in the response to aid the user in language learning.

    ### Args:
        - `update`: TelegramUpdatePing
            An object containing update information, including the chat and user details, as well as the user message text.

    ### Returns:
        - `response`: AIResponse
            The language model's response to the user's message, formatted as an `AIResponse` object.

    ### How does the function work:
        - Initializes a `LLMMessageLog` with a system message containing instructions for the bot's behavior and user information.
        - Extends the log with the last 5 messages from the chat history by calling `format_telegram_chat_history`.
        - Appends the user's latest message to the log.
        - Calls `handler_generate_response` with the message log and a specific language model (OpenAI GPT-3.5 Turbo) to generate a response.
        - Returns the generated `AIResponse`.
    """

    messages = LLMMessageLog(
        messages=[
            LLMMessage(
                role=LLMRoles.SYSTEM,
                content=f"""Your name is QuickLingoBot. You are a english langauge teacher and a helper for native persian speaker who wish to learn English. You'll be talking with them on a text chat. Focus on helping the user with thier questions. Help them in english and in persian. Be friendly, but assertive. You are an english teacher, so don't talk about anything that you wouldn't talk about in a casual classroom. In your response, make sure to include a persian translation of the english version as well. That way, users who don't english well can still learn something. Use telegram formatting as you'll be replying on telegram. Use emojis in your message
                
                You might be in a group chat. The user who sent the last message is @{update.message.from_.username or update.message.from_.first_name or 'friend'}. Only tag this user if you want to tag them. """,
            ),
        ]
    )

    messages.messages.extend(format_telegram_chat_history(update))
    messages.messages.append(
        LLMMessage(role=LLMRoles.USER, content=update.message.text)
    )

    response = handler_generate_response(messages, ValidLLMModels.OPENAI_GPT4o_MINI)
    return response


if __name__ == "__main__":
    response = handler_generate_response(
        messages=LLMMessageLog(
            messages=[LLMMessage(role=LLMRoles.SYSTEM, content="Say hello")]
        ),
        model=ValidLLMModels.OPENAI_GPT4o_MINI,
    )

    print(response.model_dump_json())

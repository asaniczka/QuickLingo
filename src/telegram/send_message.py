"""Module to get updates from telegram"""

import os

import httpx
from rich import print
from dotenv import load_dotenv
from wrapworks import cwdtoenv

load_dotenv()
cwdtoenv()


from src.models.telegram_update_models import (
    TelegramUpdatePing,
    TelegramUpdateNewMember,
)


def get_updates():
    """
    ### Responsibility:
        - Fetch the latest updates from the Telegram bot API.
        - Print the raw response text from the API call.

    ### Raises:
        - `httpx.HTTPStatusError`: If the request to the Telegram API fails.

    ### How does the function work:
        - Makes an HTTP GET request to the Telegram bot API.
        - Uses an environment variable for the bot token.
        - Prints the response text from the API call.
    """

    res = httpx.get(f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/getUpdates")
    print(res.text)


def send_welcome_message(update: TelegramUpdateNewMember) -> str:
    """
    ### Responsibility:
        - Send a welcome message to a new member in the chat.
        - Print a confirmation when the message is successfully sent.
        - Handle and log errors related to parsing the API response.

    ### Args:
        - `update`: TelegramUpdateNewMember
            Contains information about the new member and the chat, including IDs and usernames.

    ### Returns:
        - `str`
            Confirmation string indicating that the welcome message has been sent.

    ### How does the function work:
        - Constructs the base URL for the Telegram bot API and message parameters.
        - Sends an HTTP POST request with the welcome message and chat ID to the Telegram bot API.
        - Prints a confirmation message once the message is sent.
        - Attempts to parse the API response into a `TelegramUpdatePing` object.
        - Logs any parsing errors and prints detailed error information.
    """

    base_url = f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/sendMessage"
    params = {
        "chat_id": update.message.chat.id,
        "text": f"👋 سلام @{update.message.new_chat_member.username or update.message.new_chat_member.first_name}, خوش آمدید!! 🎉 من QuickLingoBot هستم🤖 و اینجا هستم که بهت کمک کنم انگلیسی یاد بگیری📚. من رو @QuickLingoBot تو پیامت تگ کن و هر سوالی داری ازم بپرس💬",
    }
    res = httpx.post(base_url, params=params)
    print("Message sent")
    try:
        _ = TelegramUpdatePing(**res.json())
    except Exception as e:
        print(
            f"Error in parsing my reply: {type(e)}: {e}\n{res.status_code} - {res.text}"
        )

    return "Welcome message sent"


def send_message(
    update: TelegramUpdatePing, response: str
) -> TelegramUpdatePing | None:
    """
    ### Responsibility:
        - Send a custom response message to a specific chat in the Telegram bot.
        - Return the parsed response from the Telegram API or raise an error if parsing fails.

    ### Args:
        - `update`: TelegramUpdatePing
            Contains information about the incoming message and the chat, including IDs.
        - `response`: str
            The response message to be sent to the chat.

    ### Returns:
        - `formatted_response`: TelegramUpdatePing | None
            Parsed API response as a `TelegramUpdatePing` object if successful; otherwise, None.

    ### Raises:
        - `AttributeError`:
            If there is an error parsing the API response.

    ### How does the function work:
        - Constructs the base URL for the Telegram bot API and message parameters.
        - Sends an HTTP POST request with the response message, chat ID, and reply-to message ID to the Telegram bot API.
        - Prints a confirmation message once the message is sent.
        - Attempts to parse the API response into a `TelegramUpdatePing` object.
        - Logs any parsing errors and raises an `AttributeError` if parsing fails.
    """

    base_url = f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/sendMessage"

    # # TESTING
    # chat_id = -865047911
    # message = "Hello @KnotAsaniczka"
    # params = {
    #     "chat_id": chat_id,
    #     "text": message,
    # }
    params = {
        "chat_id": update.message.chat.id,
        "text": response,
        "reply_to_message_id": update.message.message_id,
    }
    res = httpx.post(base_url, params=params)
    print("Message sent")
    formatted_response = None
    try:
        formatted_response = TelegramUpdatePing(**res.json())
    except Exception as e:
        print(f"Error in parsing my reply: {type(e)}: {e}")
        raise AttributeError(res.json()) from e

    return formatted_response


if __name__ == "__main__":
    send_message(1, 1)

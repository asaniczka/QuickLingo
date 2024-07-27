import os

import httpx
from dotenv import load_dotenv

load_dotenv()


def set_webhook():
    """
    ### Responsibility:
        - Set the webhook for the Telegram bot to a specified URL.
        - Print the response text from the Telegram API.

    ### How does the function work:
        - Constructs the URL for the webhook by appending "/updates" to the WEBHOOK_DOMAIN environment variable.
        - Sends an HTTP GET request to the Telegram bot API with the constructed URL as a parameter.
        - Prints the response text from the API call.
    """

    url = os.getenv("WEBHOOK_DOMAIN") + "/updates"
    
    print(url)
    params = {"url": url}
    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/setWebhook",
        params=params,
    )
    print(res.text)


def delete_webhook():
    """
    ### Responsibility:
        - Delete the current webhook for the Telegram bot.
        - Print the response text from the Telegram API.

    ### How does the function work:
        - Sends an HTTP GET request to the Telegram bot API to delete the webhook.
        - Prints the response text from the API call.
    """

    print(os.getenv("TELBOTKEY"))
    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/deleteWebhook"
    )
    print(res.text)


if __name__ == "__main__":
    delete_webhook()
    set_webhook()

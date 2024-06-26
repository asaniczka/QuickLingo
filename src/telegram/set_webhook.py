import os

import httpx


def set_webhook():

    domain = "https://romantic-lobster-genuine.ngrok-free.app"
    url = domain + "/updates"

    params = {"url": url}
    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/setWebhook",
        params=params,
    )
    print(res.text)


def delete_webhook():

    domain = "ep_2iNzEveW0WCQrZDE4ITl7Fw64Ne"
    res = httpx.get(
        f"https://api.telegram.org/bot{os.getenv('TELBOTKEY')}/deleteWebhook"
    )
    print(res.text)


if __name__ == "__main__":
    delete_webhook()
    set_webhook()

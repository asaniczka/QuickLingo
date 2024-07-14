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
    """"""

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
    """"""

    response = invoke_openai(model, messages)
    response.calculate_cost(model.value, LLM_COST_PER_TOKEN)

    return response


def remove_handles_from_message(message: str) -> str:
    """"""

    pattern = re.compile(r"(@\w+)")

    message = re.sub(pattern, "", message)
    return message


def format_telegram_chat_history(update: TelegramUpdatePing) -> list[LLMMessage]:
    """"""

    messages = get_last_n_messages(update.message.chat.id, update.message.from_.id, n=5)

    return [LLMMessage(role=x.role, content=x.message) for x in messages]


def entry_generate_response_from_user_message(update: TelegramUpdatePing) -> AIResponse:
    """"""

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

    response = handler_generate_response(messages, ValidLLMModels.OPENAI_GPT35_TURBO)
    return response


if __name__ == "__main__":
    response = handler_generate_response(
        messages=LLMMessageLog(
            messages=[LLMMessage(role=LLMRoles.SYSTEM, content="Say hello")]
        ),
        model=ValidLLMModels.OPENAI_GPT35_TURBO,
    )

    print(response.model_dump_json())

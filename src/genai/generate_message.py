"""
Issue requests to LLM using dynamic prompts
"""

from enum import Enum
import os
from datetime import datetime
import json

import httpx
from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print


cwdtoenv()
load_dotenv()

from src.models.gen_ai_models import (
    ValidLLMModels,
    LLM_COST_PER_TOKEN,
    LLMMessage,
    LLMMessageLog,
    AIResponse,
    LLMRoles,
)
from src.models.update_models import TelegramUpdatePing


def invoke_openai(model: ValidLLMModels | str, messages: LLMMessageLog) -> AIResponse:
    """"""

    if not isinstance(model, str):
        model = model.value

    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [x.model_dump() for x in messages.messages],
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


def entry_generate_response_from_user_message(update: TelegramUpdatePing) -> str:

    messages = LLMMessageLog(
        messages=[
            LLMMessage(
                role=LLMRoles.SYSTEM,
                content="Your name is QuickLingoBot. You are a english langauge teacher and a helper for native persian speaker who wish to learn English. You'll be talking with them on a text chat. Reply to them and be helpful. Focus only on english and not anything else. If the user asks questions unrelated to english learning, say you prefer to help them with english. Be friendly, but assertive.",
            ),
            LLMMessage(role=LLMRoles.USER, content=update.message.text),
        ]
    )

    response = handler_generate_response(messages, ValidLLMModels.OPENAI_GPT35_TURBO)
    return response.text


if __name__ == "__main__":
    response = handler_generate_response(
        messages=LLMMessageLog(
            messages=[LLMMessage(role=LLMRoles.SYSTEM, content="Say hello")]
        ),
        model=ValidLLMModels.OPENAI_GPT35_TURBO,
    )

    print(response.model_dump_json())

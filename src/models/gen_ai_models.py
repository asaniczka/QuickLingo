from enum import Enum
from datetime import datetime

from wrapworks import cwdtoenv
from dotenv import load_dotenv
from rich import print
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    AliasPath,
    AliasChoices,
    model_validator,
)

cwdtoenv()
load_dotenv()

LLM_COST_PER_TOKEN = {
    "gpt-4o": {"input": 0.000005, "output": 0.000015},
    "gpt-4o-mini": {"input": 0.000000150, "output": 0.000000600},
    "gpt-3.5-turbo": {"input": 0.0000005, "output": 0.0000015},
}


class ValidLLMModels(Enum):
    OPENAI_GPT4o = "gpt-4o"
    OPENAI_GPT4o_MINI = "gpt-4o-mini"
    OPENAI_GPT35_TURBO = "gpt-3.5-turbo"


class LLMRoles(Enum):
    SYSTEM = "system"
    USER = "user"
    AI = "assistant"


class LLMMessage(BaseModel):
    """Model that stores the rendered template"""

    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    role: LLMRoles
    content: str


class LLMMessageLog(BaseModel):
    """Model that stores the rendered messages"""

    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    messages: list[LLMMessage] = []


class AIResponse(BaseModel):
    text: str = Field(
        validation_alias=AliasChoices(
            AliasPath("choices", 0, "message", "content"),
        )
    )
    input_tokens: int = Field(
        validation_alias=AliasChoices(
            AliasPath("usage", "prompt_tokens"),
        )
    )
    output_tokens: int = Field(
        validation_alias=AliasChoices(
            AliasPath("usage", "completion_tokens"),
        )
    )
    cost: float | None = None

    def calculate_cost(self, model: str, cpt_table: dict):
        """Calculates the usage cost"""

        current_model = cpt_table[model]
        input_cost = current_model["input"] * self.input_tokens
        output_cost = current_model["output"] * self.output_tokens
        self.cost = input_cost + output_cost

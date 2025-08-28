import json
from typing import Any
from openai import OpenAI
from pydantic import ValidationError
from .schemas import GoldResponse


class OpenAIProvider:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model


    def generate(self, system_prompt: str, user_message: str) -> GoldResponse:
        # JSON-only response using JSON mode; we'll still validate locally with Pydantic
        resp = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        content = resp.choices[0].message.content
        try:
            data: Any = json.loads(content)
            return GoldResponse.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
        # Fallback when the model returns invalid JSON
            return GoldResponse(
                answer=("Sorry, I couldn't parse that. Please ask about digital gold. "),
                action="NOT_GOLD",
                slots={},
                follow_up=None,
            )
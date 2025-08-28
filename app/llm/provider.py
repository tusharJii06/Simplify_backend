from abc import ABC, abstractmethod
from .schemas import GoldResponse


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_message: str) -> GoldResponse:
        pass
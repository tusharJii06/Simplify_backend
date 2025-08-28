from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Gold AI Backend"
    ENV: str = "local"

    # LLM
    LLM_PROVIDER: str = "openai" # future: "ollama", "together", etc.
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Prompts
    SYSTEM_PROMPT_PATH: str = "prompts/gold_assistant.system.md"

    class Config:
        env_file = ".env"


aaa_settings = None

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
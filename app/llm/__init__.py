from .openai_client import OpenAIProvider
from .schemas import GoldResponse
from ..config import get_settings
from ..utils.file_loader import read_text_file

def get_llm_provider():
    s = get_settings()
    if s.LLM_PROVIDER == "openai":
        return OpenAIProvider(api_key=s.OPENAI_API_KEY, model=s.OPENAI_MODEL)
    else:
        raise ValueError(f"Unsupported LLM provider: {s.LLM_PROVIDER}")

def run_llm(user_message: str) -> GoldResponse:
    s = get_settings()
    system_prompt = read_text_file(s.SYSTEM_PROMPT_PATH)
    provider = get_llm_provider()
    return provider.generate(system_prompt, user_message)

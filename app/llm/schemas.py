from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal


Action = Literal[
    "NOT_GOLD",
    "INFO",
    "BUY_PROMPT",
    "COLLECT_AMOUNT",
    "COLLECT_CONFIRMATION",
    "CALL_PURCHASE_API",
]


class Slots(BaseModel):
    amount: Optional[float] = None
    user_id: Optional[str] = None


class GoldResponse(BaseModel):
    answer: str = Field(..., description="Text to show user")
    action: Action
    slots: Slots = Field(default_factory=Slots)
    follow_up: Optional[str] = None
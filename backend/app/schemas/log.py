from datetime import datetime
from typing import Any
from pydantic import BaseModel


class LogRead(BaseModel):
    id: int
    user_id: int | None = None
    action: str
    timestamp: datetime
    meta: dict[str, Any] | None = None

    class Config:
        orm_mode = True 
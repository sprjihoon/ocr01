from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class PriceHistoryBase(BaseModel):
    product_code: str | None = None
    product_name: str
    price: Decimal
    event_info: str | None = None


class PriceHistoryRead(PriceHistoryBase):
    id: int
    image_id: int
    user_id: int
    store_id: int
    date: date
    badge7: bool | None = None
    badge30: bool | None = None

    class Config:
        orm_mode = True 
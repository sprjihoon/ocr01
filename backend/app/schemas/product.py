from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    code: Optional[str] = None
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True 
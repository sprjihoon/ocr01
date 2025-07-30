from pydantic import BaseModel


class StoreBase(BaseModel):
    name: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    zone: str | None = None


class StoreCreate(StoreBase):
    pass


class StoreRead(StoreBase):
    id: int

    class Config:
        orm_mode = True 
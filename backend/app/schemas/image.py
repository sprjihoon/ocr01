from datetime import datetime
from pydantic import BaseModel


class ImageBase(BaseModel):
    store_id: int
    zone: str | None = None


class ImageCreate(ImageBase):
    pass  # file upload handled separately


class ImageRead(ImageBase):
    id: int
    user_id: int
    upload_time: datetime
    image_url: str

    class Config:
        orm_mode = True 


class PresignedRequest(BaseModel):
    filename: str
    content_type: str = "image/jpeg"


class PresignedResponse(BaseModel):
    key: str
    url: str
    fields: dict[str, str]


class ImageComplete(BaseModel):
    store_id: int
    zone: str
    key: str
    image_url: str 
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    is_admin: bool = False


class UserRead(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True 
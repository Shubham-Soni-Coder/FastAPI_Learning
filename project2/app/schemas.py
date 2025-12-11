# schemas.py
from pydantic import BaseModel
from datetime import datetime


class Usermodel(BaseModel):
    id: int
    username: str
    gmail_id: str
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    gmail_id: str
    password: str
    is_admin: bool = False

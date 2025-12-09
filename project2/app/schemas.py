# schemas.py
from pydantic import BaseModel
from datatime import datatime


class Usermodel(BaseModel):
    id: int
    username: str
    gmail_id: str
    password: str
    created_at: datatime

    class config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    gmail_id: str
    password: str
    is_admin: bool = False

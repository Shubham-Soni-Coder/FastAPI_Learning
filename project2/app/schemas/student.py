from pydantic import BaseModel
from typing import Optional


class StudentCreate(BaseModel):
    roll_no: Optional[str] = None
    name: str
    father_name: str
    mother_name: str
    email: str
    hashed_password: str
    class_id: int
    is_active: bool


class StudentRespone(BaseModel):
    id: int
    name: str
    class_id: int

    class Config:
        from_attributes = True

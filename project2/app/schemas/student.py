from pydantic import BaseModel
from typing import Optional


class StudentCreate(BaseModel):
    user_id: int
    roll_no: Optional[str] = None
    class_id: int

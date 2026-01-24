from pydantic import BaseModel
from typing import Optional


class StudentCreate(BaseModel):
    user_id: int
    class_id: int
    name: str
    father_name: str
    mother_name: str
    roll_no: Optional[str] = None

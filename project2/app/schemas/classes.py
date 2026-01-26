from pydantic import BaseModel
from datetime import datetime


# ------------Base---------
class ClassBase(BaseModel):
    name: str
    subject: str

    teacher_id: int

    start_time: datetime
    end_time: datetime

    is_active = bool = True


# --------Create-------
class ClassCreate(BaseModel):
    pass


# --------Update--------
class ClassUpdate(BaseModel):
    subject: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    is_active: bool | None = None


# ------Respone----------
class ClassOut(ClassBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

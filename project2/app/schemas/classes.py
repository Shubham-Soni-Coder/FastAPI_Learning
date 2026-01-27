from pydantic import BaseModel, ConfigDict
from datetime import datetime


# ------------Base---------
class ClassBase(BaseModel):
    name: str
    subject: str

    teacher_id: int
    batch_id: int

    start_time: datetime
    end_time: datetime


# --------Create-------
class ClassCreate(ClassBase):
    pass


# --------Update--------
class ClassUpdate(ClassBase):
    subject: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


# ------Respone----------
class ClassOut(ClassBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class AttendanceSessionCreate(BaseModel):
    class_id: int
    date: date
    session_name: str


class AttendanceRecordCreate(BaseModel):
    session_id: int
    student_id: int
    status: str
    remark: Optional[str] = None


class AttendanceItemCreate(BaseModel):
    student_id: int
    is_present: bool


class AttendanceSubmitCreate(BaseModel):
    class_id: int
    date: date
    session_type: str
    attendance: List[AttendanceItemCreate]

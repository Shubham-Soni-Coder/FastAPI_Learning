from pydantic import BaseModel
from typing import Optional, List


class ClassCreate(BaseModel):
    class_name: str
    stream: Optional[str] = None


class SubjectCreate(BaseModel):
    name: str


class ClassSubjectCreate(BaseModel):
    class_id: int
    subject_id: int
    category: str
    stream: Optional[str] = None
    is_compulsory: Optional[bool] = False
    is_main: Optional[bool] = False


class StudentSubjectSelect(BaseModel):
    subjects_id: List[int]

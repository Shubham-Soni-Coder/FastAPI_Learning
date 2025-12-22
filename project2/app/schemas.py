# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Usermodel(BaseModel):
    id: int
    gmail_id: str
    password: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    gmail_id: str
    password: str
    is_admin: bool = False


class OTP(BaseModel):
    gmail_id: str
    otp_hash: str
    expires_at: datetime


class ClassCreate(BaseModel):
    class_name: str
    stream: Optional[str] = None


class StudentCreate(BaseModel):
    roll_no: str
    name: str
    father_name: str
    mother_name: str
    email: str
    hashed_password: str
    class_id: int
    is_active: bool


class SubjectCreate(BaseModel):
    name: str


class ClassSubjectCreate(BaseModel):
    class_id: int
    subject_id: int


class StudentSubjectSelect(BaseModel):
    subjects_id: List[int]


class StudentRespone(BaseModel):
    id: int
    name: str
    class_id: int

    class Config:
        from_attributes = True


class FeesStructureCreate(BaseModel):
    class_id: int
    academic_year: str
    is_active: bool


class FeesComponentCreate(BaseModel):
    fees_structure_id: int
    compound_name: str
    amount: int

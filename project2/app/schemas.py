"""
Schemas Module
==============

This module defines Pydantic models (schemas) for data validation and serialization.
It includes schemas for User creation, OTP verification, Student data, and Fee structures.
"""

from pydantic import BaseModel
from datetime import datetime, date
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
    roll_no: Optional[str] = None

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
    is_optional: Optional[bool] = False


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
    component_name: str
    amount: int


class StudentFeesDueCreate(BaseModel):
    student_id: int
    month: int
    year: int
    total_amount: float
    status: str


class FeesPaymentCreate(BaseModel):
    due_id: int
    amount_paid: float
    discount_amount: float
    fine_amount: float
    method: str
    is_late: bool


class AttendanceSessionCreate(BaseModel):
    class_id: int
    date: date
    session_name: str


class AttendanceRecordCreate(BaseModel):
    session_id: int
    student_id: int
    status: str
    remark: Optional[str] = None

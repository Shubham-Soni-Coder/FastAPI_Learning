from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(20), nullable=False)  # use pydamtic for range
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(50), index=True, nullable=False)
    otp_hash = Column(String(120), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(50), nullable=False)
    stream = Column(String(10), nullable=True)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(Integer, nullable=True)
    name = Column(String(50), nullable=False)
    father_name = Column(String(30), nullable=False)
    mother_name = Column(String(30), nullable=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(500), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    is_active = Column(Boolean, default=False)
    class_ = relationship("Class", backref="students")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class ClassSubject(Base):
    __tablename__ = "class_subjects"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)

    is_optional = Column(Boolean, default=False)
    __table_args__ = (
        UniqueConstraint("class_id", "subject_id", name="uix_class_subject"),
    )


class StudentSubject(Base):
    __tablename__ = "student_subjects"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", name="uix_student_subject"),
    )
    student = relationship("Student", backref="student_subjects")
    subject = relationship("Subject")


class FeesStructure(Base):
    __tablename__ = "fees_structure"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    academic_year = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    components = relationship(
        "FeesComponent", back_populates="fees_structure", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("class_id", "academic_year", name="uq_class_year"),
    )


class FeesComponent(Base):
    __tablename__ = "fees_components"
    id = Column(Integer, primary_key=True, index=True)
    fees_structure_id = Column(Integer, ForeignKey("fees_structure.id"), nullable=False)
    compound_name = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)

    fees_structure = relationship("FeesStructure", back_populates="components")

    __table_args__ = (
        UniqueConstraint(
            "fees_structure_id", "component_name", name="uq_structure_component"
        ),
    )

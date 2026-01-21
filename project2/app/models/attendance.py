from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
)
from app.database.base import Base
from datetime import datetime


class AttendanceSession(Base):
    __tablename__ = "attendance_session"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))

    date = Column(Date, nullable=False)
    session_name = Column(
        String(50), default="morning"
    )  # Session -> Morning , Evening , exam , etc
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "class_id", "date", "session_name", name="uq_class_date_session"
        ),
    )


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_session.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    status = Column(
        Enum("present", "absent", "late", "leave", name="attendance_status"),
        nullable=False,
    )
    remark = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("session_id", "student_id", name="uq_session_student"),
    )

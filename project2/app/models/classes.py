from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from app.database.base import Base
from sqlalchemy.sql import func


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

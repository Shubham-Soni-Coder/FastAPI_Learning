from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Time,
    Date,
    CheckConstraint,
    UniqueConstraint,
)
from app.database.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

    batch_id = Column(Integer, ForeignKey("batches.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True)

    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)

    # 1.Mondey .... 7.Sunday
    day_of_week = Column(Integer, nullable=False)

    name = Column(String, nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    batch = relationship("Batches")
    teacher = relationship("Teacher")
    subject = relationship("Subject")

    __table_args__ = (
        CheckConstraint(
            "day_of_week BETWEEN 1 AND 7", name="ck_class_schedule_day_of_week"
        ),
        CheckConstraint(
            "start_time < end_time", name="ck_class_schedule_start_end_time"
        ),
    )


class ClassInstance(Base):
    __tablename__ = "class_instances"

    id = Column(Integer, primary_key=True)

    schedule_id = Column(
        Integer, ForeignKey("class_schedules.id", ondelete="CASCADE"), nullable=False
    )

    class_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)

    schedule = relationship("ClassSchedule", backref="class_instances")

    __table_args__ = (
        CheckConstraint(
            "status IN ('held','cancelled','rescheduled')",
            name="ck_class_instance_status",
        ),
        UniqueConstraint(
            "schedule_id", "class_date", name="uq_class_instance_schedule_date"
        ),
    )

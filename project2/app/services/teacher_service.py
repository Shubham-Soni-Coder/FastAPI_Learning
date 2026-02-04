from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import Student, StudentFeesDue, Batches, ClassSchedule
from app.utils.helpers import initials
from app.utils.data_utils import get_total_days_in_month
from app.services.attendance_service import count_student_present_day
from datetime import time


def get_students_for_batch(db: Session, batch_id: int, month: int, year: int):
    total_days = get_total_days_in_month(year, month)

    results = (
        db.query(Student, StudentFeesDue)
        .join(Batches, Student.batch_id == Batches.id)
        .join(StudentFeesDue, Student.id == StudentFeesDue.student_id)
        .filter(Batches.id == batch_id)
        .order_by(Student.name.asc())
        .all()
    )

    students_data = []

    for i, (student, fees) in enumerate(results):
        days_present = count_student_present_day(db, student.id, year, month)

        attendance_percentage = (
            round((days_present / total_days) * 100) if total_days > 0 else 0
        )

        students_data.append(
            {
                "roll_no": i + 1,
                "name": student.name,
                "initials": initials(student.name),
                "father_name": student.father_name,
                "fees_paid": fees.status if fees else "pending",
                "days_present": days_present,
                "total_days": total_days,
                "attendance": attendance_percentage,
            }
        )
    return students_data


def get_active_classes(db: Session, teacher_id: int, day: int, current_time: time):
    """
    Get classes that are currently happening (Start <= Now <= End)
    """
    schedules = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher_id,
            ClassSchedule.day_of_week == day,
            ClassSchedule.start_time <= current_time,
            ClassSchedule.end_time >= current_time,
        )
        .all()
    )
    return schedules


def get_upcoming_classes(db: Session, teacher_id: int, day: int, current_time: time):
    """
    Get classes that will start later today (Start > Now)
    """
    schedules = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher_id,
            ClassSchedule.day_of_week == day,
            ClassSchedule.start_time > current_time,
        )
        .order_by(ClassSchedule.start_time.asc())
        .all()
    )
    return schedules

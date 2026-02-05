from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from app.models import Student, StudentFeesDue, Batches, ClassSchedule, Teacher, Subject
from app.utils.helpers import initials
from app.utils.data_utils import get_total_days_in_month
from app.services.attendance_service import count_student_present_day
from datetime import time, datetime


def get_students_for_batch(db: Session, batch_id: int, month: int, year: int):
    total_days = get_total_days_in_month(year, month)

    results = (
        db.query(Student, StudentFeesDue)
        .join(Batches, Student.batch_id == Batches.id)
        .outerjoin(
            StudentFeesDue,
            and_(
                Student.id == StudentFeesDue.student_id,
                StudentFeesDue.month == month,
                StudentFeesDue.year == year,
            ),
        )
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
                "fees_paid": True if fees and fees.status == "paid" else False,
                "days_present": days_present,
                "total_days": total_days,
                "attendance": attendance_percentage,
            }
        )
    return students_data


def get_teacher_dashboard_stats(db: Session, teacher_id: int):
    """Calculate dynamic stats for teacher dashboard"""
    total_classes = (
        db.query(func.count(ClassSchedule.id))
        .filter(ClassSchedule.teacher_id == teacher_id)
        .scalar()
    )

    # Get teacher's unique batches
    batch_ids = (
        db.query(ClassSchedule.batch_id)
        .filter(ClassSchedule.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    batch_ids = [r[0] for r in batch_ids]

    total_students = (
        db.query(func.count(Student.id))
        .filter(Student.batch_id.in_(batch_ids))
        .scalar()
        if batch_ids
        else 0
    )

    return {
        "total_students": total_students,
        "active_classes": total_classes,
        "pending_review": 12,  # Placeholder
        "rating": 4.8,  # Placeholder
    }


def is_teacher_authorized(db: Session, teacher_id: int, batch_id: int) -> bool:
    """Verify if a teacher is assigned to a specific batch"""
    return (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher_id, ClassSchedule.batch_id == batch_id
        )
        .first()
        is not None
    )


def get_teacher_batches_list(db: Session, teacher_id: int):
    """Get unique list of batches for a teacher"""
    schedules = (
        db.query(ClassSchedule).filter(ClassSchedule.teacher_id == teacher_id).all()
    )

    unique_batches = {}
    for s in schedules:
        if s.batch_id not in unique_batches:
            unique_batches[s.batch_id] = s.batch.batch_name

    return [
        {"id": bid, "name": bname} for bid, bname in unique_batches.items()
    ], unique_batches


def get_formatted_upcoming_classes(
    db: Session, teacher_id: int, day: int, current_time: time
):
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

    formatted = []
    for cls in schedules:
        student_count = (
            db.query(func.count(Student.id))
            .filter(Student.batch_id == cls.batch_id)
            .scalar()
        )
        formatted.append(
            {
                "batch_id": cls.batch_id,
                "batch_name": cls.batch.batch_name if cls.batch else "Class",
                "subject": cls.subject.name if cls.subject else "N/A",
                "time": cls.start_time.strftime("%I:%M %p"),
                "student_count": student_count,
            }
        )
    return formatted


def get_all_classes_formatted(db: Session, teacher_id: int):
    classes = (
        db.query(ClassSchedule).filter(ClassSchedule.teacher_id == teacher_id).all()
    )

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    results = []

    for cls in classes:
        student_count = (
            db.query(func.count(Student.id))
            .filter(Student.batch_id == cls.batch_id)
            .scalar()
        )
        day_name = days[cls.day_of_week - 1] if 1 <= cls.day_of_week <= 7 else "Unknown"

        results.append(
            {
                "id": cls.batch_id,
                "name": cls.name,
                "subject": cls.subject.name,
                "students": student_count,
                "time": (
                    f"{day_name} {cls.start_time.strftime('%I:%M %p')}"
                    if cls.start_time
                    else "N/A"
                ),
                "day_code": cls.day_of_week,
            }
        )
    return results


def get_active_classes(db: Session, teacher_id: int, day: int, current_time: time):
    """Get classes that are currently happening"""
    return (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher_id,
            ClassSchedule.day_of_week == day,
            ClassSchedule.start_time <= current_time,
            ClassSchedule.end_time >= current_time,
        )
        .all()
    )


def get_upcoming_classes(db: Session, teacher_id: int, day: int, current_time: time):
    """Raw upcoming classes"""
    return (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher_id,
            ClassSchedule.day_of_week == day,
            ClassSchedule.start_time > current_time,
        )
        .order_by(ClassSchedule.start_time.asc())
        .all()
    )

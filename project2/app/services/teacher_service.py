from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import Student, StudentFeesDue, Batches
from app.utils.helpers import initials
from app.utils.data_utils import get_total_days_in_month
from app.services.attendance_service import count_student_present_day


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

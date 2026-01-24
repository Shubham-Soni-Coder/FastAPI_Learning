from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import Student, AttendanceSession, AttendanceRecord
from app.schemas.attendance import AttendanceRecordCreate
import random

# store in database
Base.metadata.create_all(bind=engine)

# make a db
db = SessionLocal()


def create_attendance_record():
    class_id = 11
    session_ids = [
        i[0]
        for i in db.query(AttendanceSession.id)
        .filter(AttendanceSession.class_id == class_id)
        .all()
    ]
    student_ids = [
        i[0] for i in db.query(Student.id).filter(Student.class_id == class_id).all()
    ]

    records = []

    for session_id in session_ids:
        for student_id in student_ids:
            schems = AttendanceRecordCreate(
                session_id=session_id,
                student_id=student_id,
                status=random.choice(["present", "absent"]),
            )
            model = AttendanceRecord(**schems.model_dump())
            records.append(model)
    db.add_all(records)
    db.commit()

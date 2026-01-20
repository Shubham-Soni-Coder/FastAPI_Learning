from fastapi import APIRouter, Depends, HTTPException
from app.schemas import (
    AttendanceSubmitCreate,
    AttendanceItemCreate,
    AttendanceSessionCreate,
    AttendanceRecordCreate,
)
from app.models import AttendanceSession, AttendanceRecord, Student
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api")


@router.post("/attendance")
def save_attendance(payload: AttendanceSubmitCreate, db: Session = Depends(get_db)):
    # 1. Find or create session
    session = (
        db.query(AttendanceSession)
        .filter(
            AttendanceSession.class_id == payload.class_id,
            AttendanceSession.date == payload.date,
            AttendanceSession.session_name == payload.session_type,
        )
        .first()
    )

    # check for session
    if not session:
        schems = AttendanceSessionCreate(
            class_id=payload.class_id,
            date=payload.date,
            session_name=payload.session_type,
        )
        session = AttendanceSession(**schems.dict())
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Save/Update attendance records
    for item in payload.attendance:
        # optional safety : check for the student beylong to class
        student = (
            db.query(Student)
            .filter(Student.id == item.student_id, Student.class_id == payload.class_id)
            .first()
        )

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        record = (
            db.query(AttendanceRecord)
            .filter(
                AttendanceRecord.session_id == session.id,
                AttendanceRecord.student_id == item.student_id,
            )
            .first()
        )
        if item.is_present:
            status = "present"
        else:
            with open("AttendanceError.txt", "a") as f:
                f.write(f"{item.is_present}\n")
            status = "absent"

        if record:
            record.status = status
        else:
            schems = AttendanceRecordCreate(
                session_id=session.id, student_id=item.student_id, status=status
            )
            record = AttendanceRecord(**schems.dict())
            db.add(record)
    db.commit()

    return {"message": "Attendance saved successfully", "session_id": session.id}

from sqlalchemy import func, distinct
from app.models import AttendanceSession, AttendanceRecord
import json


def count_student_present_day(db, student_id: int, year: int, month: int) -> int:
    present_day = (
        db.query(func.count(distinct(AttendanceSession.date)))
        .join(AttendanceRecord, AttendanceRecord.session_id == AttendanceSession.id)
        .filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.status == "present",
            func.strftime("%Y", AttendanceSession.date) == str(year),
            func.strftime("%m", AttendanceSession.date) == f"{month:02d}",
        )
        .scalar()
    )
    return present_day


def load_data():
    with open("demo.json", "r", encoding="utf-8") as f:
        JSON_DATA = json.load(f)
    return JSON_DATA

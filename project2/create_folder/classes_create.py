from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import Subject, ClassSchedule
from app.utils.json_loader import load_json
from app.schemas.classes import ClassScheduleCreate
from datetime import time, datetime


# load the student data
# JSON_DATA = load_json()

# # store in database
Base.metadata.create_all(bind=engine)


# make a db
db = SessionLocal()


def add_data_classes(JSON_DATA):
    JSON_DATA = JSON_DATA["class_schedules"]

    for data in JSON_DATA:

        subject = db.query(Subject).filter(Subject.name == data["subject"]).first()

        if subject is None:
            raise ValueError("Subject not found")

        subject_id = subject.id  # get the integer ID

        schems = ClassScheduleCreate(
            batch_id=data["batch_id"],
            teacher_id=data["teacher_id"],
            subject_id=subject_id,
            day_of_week=data["day_of_week"],
            name=data["name"],
            start_time=datetime.strptime(data["start_time"], "%H:%M:%S").time(),
            end_time=datetime.strptime(data["end_time"], "%H:%M:%S").time(),
        )
        model = ClassSchedule(**schems.dict())
        db.add(model)
    db.commit()


def check_for_active_classes(day, time):
    schedules = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.day_of_week == day,
            ClassSchedule.start_time <= time,
            ClassSchedule.end_time >= time,
        )
        .all()
    )

    return schedules


def check_for_upcoming_classes(day, time):
    schedules = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.day_of_week == day,
            ClassSchedule.start_time > time,
        )
        .all()
    )

    return schedules

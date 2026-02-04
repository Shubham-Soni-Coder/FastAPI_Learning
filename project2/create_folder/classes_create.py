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
    schedules_template = JSON_DATA["class_schedules"]

    for day in range(1, 7):  # 1 (Monday) to 6 (Saturday)
        for data in schedules_template:
            subject = db.query(Subject).filter(Subject.name == data["subject"]).first()

            if subject is None:
                print(f"Subject '{data['subject']}' not found, skipping...")
                continue

            subject_id = subject.id

            schems = ClassScheduleCreate(
                batch_id=data["batch_id"],
                teacher_id=data["teacher_id"],
                subject_id=subject_id,
                day_of_week=day,  # Use the loop variable for day
                name=data["name"],
                start_time=datetime.strptime(data["start_time"], "%I:%M %p").time(),
                end_time=datetime.strptime(data["end_time"], "%I:%M %p").time(),
            )
            model = ClassSchedule(**schems.dict())
            db.add(model)
    db.commit()

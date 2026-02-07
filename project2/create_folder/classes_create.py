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


def is_overlapping(db, teacher_id, day, start_time, end_time):
    """Check if a teacher has an overlapping class on the same day"""
    overlapping = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher_id,
            ClassSchedule.day_of_week == day,
            # (StartA < EndB) AND (EndA > StartB)
            ClassSchedule.start_time < end_time,
            ClassSchedule.end_time > start_time,
        )
        .first()
    )
    return overlapping is not None


def add_data_classes(JSON_DATA):
    schedules_template = JSON_DATA["class_schedules"]

    # Clear old schedules to prevent duplicates/overlaps from previous runs
    db.query(ClassSchedule).delete()
    db.commit()
    print("Old class schedules cleared.")

    for data in schedules_template:
        # Loop for Monday (1) to Saturday (6)
        for day in range(1, 7):
            subject = db.query(Subject).filter(Subject.name == data["subject"]).first()

            if subject is None:
                print(f"Subject '{data['subject']}' not found, skipping...")
                continue

            start_t = datetime.strptime(data["start_time"], "%I:%M %p").time()
            end_t = datetime.strptime(data["end_time"], "%I:%M %p").time()

            schems = ClassScheduleCreate(
                batch_id=data["batch_id"],
                teacher_id=data["teacher_id"],
                subject_id=subject.id,
                day_of_week=day,
                name=data["name"],
                start_time=start_t,
                end_time=end_t,
            )
            model = ClassSchedule(**schems.model_dump())
            db.add(model)
        db.commit()
    print("Class schedules data added for all days (Mon-Sat).")

from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import Class, Teacher
from app.utils.json_loader import load_json
from app.schemas.classes import ClassCreate
from datetime import datetime, date

# load the student data
JSON_DATA = load_json()
JSON_DATA = JSON_DATA["teacher_classes"]

# # store in database
Base.metadata.create_all(bind=engine)


# make a db
db = SessionLocal()


def add_data_classes(JSON_DATA):
    # first get the teacher_id
    teacher_id = list(db.query(Teacher.id).filter(Teacher.full_name == "Shubham Soni"))[
        0
    ][0]

    JSON_DATA = JSON_DATA["teacher_classes"]

    for data in JSON_DATA:
        schems = ClassCreate(
            name=data["name"],
            subject=data["subject"],
            batch_id=data["id"],
            teacher_id=teacher_id,
            start_time=datetime.strptime(
                f"{date.today()} {data['start_time']}".replace("20", ""),
                "%y-%m-%d %I:%M %p",
            ),
            end_time=datetime.strptime(
                f"{date.today()} {data['end_time']}".replace("20", ""),
                "%y-%m-%d %I:%M %p",
            ),
        )
        model = Class(**schems.model_dump())
        db.add(model)
    db.commit()

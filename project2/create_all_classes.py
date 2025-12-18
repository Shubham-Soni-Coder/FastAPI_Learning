from app.database import engine, Base, get_db, session
from app.models import (
    Base,
    User,
    Class,
    Subject,
    ClassSubject,
    Student,
    StudentSubject,
)
from app.schemas import (
    ClassCreate,
    SubjectCreate,
    StudentCreate,
)
import json

# store in database
Base.metadata.create_all(bind=engine)

db = session()


# make a constent class
def create_class():
    starting = ["1st", "2nd", "3rd"]
    after = [f"{i}th" for i in range(4, 13)]
    streams = ["non-medical", "medical", "arts", "commerce"]

    classes = starting + after

    for cl in classes:
        int_cl = int(cl[:-2])  # remove last two
        if int_cl <= 10:
            schema = ClassCreate(class_name=cl, stream=None)
            model = Class(**schema.model_dump())
            db.add(model)
        else:
            for stream in streams:
                schema = ClassCreate(class_name=cl, stream=stream)
                model = Class(**schema.model_dump())
                db.add(model)
    db.commit()


def create_student():

    with open("demo.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    classes = db.query(Class).all()

    for i, (gmail, user) in enumerate(data.items()):
        class_obj = classes[i % len(classes)]  # roation with %
        schems = StudentCreate(
            name=user["name"],
            email=gmail,
            hashed_password=user["password"],
            class_id=class_obj.id,
        )
        model = Student(**schems.model_dump())
        db.add(model)
    db.commit()


def show_data():
    data = db.query(Student).all()
    for i, user in enumerate(data):
        print(i, user.name, user.class_id)
    db.close()


def drop_table():
    from sqlalchemy import text

    db.execute(text("DROP TABLE IF EXISTS students"))
    db.commit()


if __name__ == "__main__":
    create_student()
    show_data()
    # drop_table()

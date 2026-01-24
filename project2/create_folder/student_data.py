from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import User, Class, Student
from app.schemas import UserCreate
from app.core.security import hash_password
from app.utils.json_loader import load_json
from app.schemas.student import StudentCreate

# load the student data
JSON_DATA = load_json("data.json")
JSON_DATA = JSON_DATA["students"]


# store in database
Base.metadata.create_all(bind=engine)

# make a db
db = SessionLocal()


def add_data():
    # get all the student_id from the database
    student_id = [i[0] for i in db.query(User.id).filter(User.role == "Student").all()]

    # get all the class_id from the database
    class_id = [i[0] for i in db.query(Class.id).all()]

    # add the student data to the database
    for i, user in enumerate(JSON_DATA):
        class_obj = class_id[i % len(class_id)]
        schems = StudentCreate(
            user_id=student_id[i],
            class_id=class_obj,
            name=user["name"],
            father_name=user["father_name"],
            mother_name=user["mother_name"],
        )
        model = Student(**schems.model_dump())
        db.add(model)
    db.commit()


def rename_class_id(id):
    # get the class_id  from the database
    db.query(Student).filter(Student.id == id).update({"class_id": 11})
    db.commit()

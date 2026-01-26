from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import User
from app.schemas import UserCreate
from app.core.security import hash_password
from app.utils.json_loader import load_json


# store in database
Base.metadata.create_all(bind=engine)

# make a db
db = SessionLocal()


def user_create():
    data = {
        "teacher": {"sonishubham2888@gmail.com": "Shubham@09082006"},
        "Student": {"slsitu1424@gmail.com": "Situ@09082006"},
        "Admin": {"Admin@gmail.com": "Admin@09082006"},
    }
    for role, user in data.items():
        for email, password in user.items():
            schems = UserCreate(
                gmail_id=email,
                hashed_password=hash_password(password),
                is_active=True,
                role=role,
            )
            model = User(**schems.model_dump())
            db.add(model)
    db.commit()


def add_student(JSON_DATA):
    JSON_DATA = JSON_DATA["students"]
    for student in JSON_DATA:
        schems = UserCreate(
            gmail_id=student["email"],
            hashed_password=hash_password(student["hashed_password"]),
            is_active=student["is_active"],
            role="Student",
        )
        model = User(**schems.model_dump())
        db.add(model)
    db.commit()


def add_teacher(JSON_DATA):
    JSON_DATA = JSON_DATA["teacher"]
    for teacher in JSON_DATA:
        schems = UserCreate(
            gmail_id=teacher["gmail"],
            hashed_password=hash_password(teacher["hashed_password"]),
            is_active=teacher["is_active"],
            role="Teacher",
        )
        model = User(**schems.model_dump())
        db.add(model)
    db.commit()


if __name__ == "__main__":
    add_data()

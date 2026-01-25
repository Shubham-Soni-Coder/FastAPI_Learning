from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models import User
from app.models import Teacher
from app.schemas.teacher import TeacherCreate
from datetime import datetime

# store in database
Base.metadata.create_all(bind=engine)

# make a db
db = SessionLocal()


def CreateTeacher():
    # get the teacher_id from database
    teacher_id = [
        id[0] for id in db.query(User.id).filter(User.role == "teacher").all()
    ]

    full_name = ["Shubham Soni"]
    department = ["Mathematics"]

    for i, id in enumerate(teacher_id):
        schems = TeacherCreate(
            user_id=id,
            full_name=full_name[i],
            department=department[i],
            is_active=True,
            created_at=datetime.now(),
        )
        model = Teacher(**schems.model_dump())
        db.add(model)
    db.commit()

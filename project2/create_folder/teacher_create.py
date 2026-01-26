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


def CreateTeacher(JSON_DATA):
    teachers_data = JSON_DATA.get("teacher", [])

    # Debug print
    print(f"Found {len(teachers_data)} teachers in JSON")

    for teacher_info in teachers_data:
        email = teacher_info.get("gmail")
        name = teacher_info.get("name")
        department = teacher_info.get("department_name")

        # Find user by email to ensure correct mapping
        user = db.query(User).filter(User.gmail_id == email).first()

        if user:
            # Check if teacher profile already exists
            existing = db.query(Teacher).filter(Teacher.user_id == user.id).first()
            if not existing:
                try:
                    schems = TeacherCreate(
                        user_id=user.id,
                        full_name=name,
                        department=department,
                        is_active=True,
                        created_at=datetime.now(),
                    )
                    model = Teacher(**schems.model_dump())
                    db.add(model)
                    print(f"Adding teacher: {name}")
                except Exception as e:
                    print(f"Error creating teacher {name}: {e}")
            else:
                print(f"Teacher {name} already exists.")
        else:
            print(f"User with email {email} not found.")

    db.commit()

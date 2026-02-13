from sqlalchemy.orm import Session
from datetime import datetime, date, time
from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.schemas import (
    UserCreate,
    TeacherCreate,
    SubjectCreate,
    BatchesCreate,
    StudentCreate,
)
from app.models import (
    User,
    Teacher,
    Subject,
    Batches,
    Student,
)
from app.core.security import hash_password
from app.utils.json_loader import load_json
from datetime import datetime

"""
All table : 
1. User : complet
2. Teachers : complet
3. subjects : complet
11. batches : complet
12. batch_subjects
5. student_fes_due
6. fees_structure
7. fees_components
8. fee_payments
9. class_scheddules
10. class_instances
13. attendance_session
14. attendance_records
"""

# load the json data
JSON_DATA = load_json()

# store in database
Base.metadata.create_all(bind=engine)

db = SessionLocal()


# create user table
class DataBaseCreate:
    def __init__(self, JSON_DATA: dict) -> None:
        self.JSON_DATA = JSON_DATA

    def CreateUser(self) -> None:
        data = {
            "student": {
                self.JSON_DATA["students"][i]["gmail"]: self.JSON_DATA["students"][i][
                    "password"
                ]
                for i in range(len(self.JSON_DATA["students"]))
            },
            "teacher": {
                self.JSON_DATA["teacher"][i]["gmail"]: self.JSON_DATA["teacher"][i][
                    "password"
                ]
                for i in range(len(self.JSON_DATA["teacher"]))
            },
        }

        for role, user in data.items():
            for email, password in user.items():
                # Check if user already exists
                existing_user = db.query(User).filter(User.gmail_id == email).first()
                if not existing_user:
                    schems = UserCreate(
                        gmail_id=email,
                        hashed_password=hash_password(password),
                        is_active=True,
                        role=role,
                    )
                    model = User(**schems.model_dump())
                    db.add(model)
                    print(f"Adding user: {email} ({role})")
                else:
                    print(f"User {email} already exists.")
            db.commit()

    def CreateTeacher(self) -> None:
        teachers_data = self.JSON_DATA.get("teacher", [])

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

    def CreateStudent(self) -> None:
        student_data = self.JSON_DATA.get("students", [])
        batches = db.query(Batches).all()

        if not batches:
            print("No batches found. Please create batches first.")
            return

        for i, user_info in enumerate(student_data):
            batch_obj = batches[i % len(batches)]
            email = user_info.get("gmail")

            # Find user by email to get user_id
            user_rec = db.query(User).filter(User.gmail_id == email).first()

            if user_rec:
                # Check if student profile already exists
                existing_student = (
                    db.query(Student).filter(Student.user_id == user_rec.id).first()
                )
                if not existing_student:
                    try:
                        schems = StudentCreate(
                            user_id=user_rec.id,
                            name=user_info["name"],
                            father_name=user_info["father_name"],
                            mother_name=user_info["mother_name"],
                            roll_no=str(user_info["roll_no"]),
                            batch_id=batch_obj.id,
                        )
                        model = Student(**schems.model_dump())
                        db.add(model)
                        print(f"Adding student: {user_info['name']}")
                    except Exception as e:
                        print(f"Error creating student {user_info['name']}: {e}")
                else:
                    print(f"Student {user_info['name']} already exists.")
            else:
                print(f"User with email {email} not found for student profiling.")

        db.commit()

    @staticmethod
    def add_subject(name: str) -> None:
        # Check if subject already exists
        existing_subject = db.query(Subject).filter(Subject.name == name).first()
        if not existing_subject:
            try:
                schems = SubjectCreate(name=name)
                model = Subject(**schems.model_dump())
                db.add(model)
                print(f"Adding subject: {name}")
            except Exception as e:
                print(f"Error creating subject {name}: {e}")
        else:
            print(f"Subject {name} already exists.")

    def CreateSubject(self) -> None:
        Subject_data = self.JSON_DATA["Subjects"]

        unique_subjects = set()

        # common
        for subject_name in Subject_data.get("Common", []):
            unique_subjects.add(subject_name)

        # optional
        for subject_name in Subject_data.get("Optional", []):
            unique_subjects.add(subject_name)

        # Stream
        for stream_subject in Subject_data.get("Streams", {}).values():
            for subject_name in stream_subject:
                unique_subjects.add(subject_name)

        # Add at once
        for name in unique_subjects:
            self.add_subject(name)
        db.commit()

    def CreateBatch(self) -> None:
        starting = ["1st", "2nd", "3rd"]
        after = [f"{i}th" for i in range(4, 13)]
        streams = ["non-medical", "medical", "arts", "commerce"]

        batches = starting + after

        for batch_name_label in batches:
            batch_level = int(batch_name_label[:-2])  # remove suffix
            # If <= 10, only one batch with stream=None, else multiple streams
            for stream in [None] if batch_level <= 10 else streams:
                # Check if batch already exists
                existing_batch = (
                    db.query(Batches)
                    .filter(
                        Batches.batch_name == batch_name_label, Batches.stream == stream
                    )
                    .first()
                )

                if not existing_batch:
                    schema = BatchesCreate(batch_name=batch_name_label, stream=stream)
                    db.add(Batches(**schema.model_dump()))
                    print(
                        f"Adding batch: {batch_name_label} ({stream if stream else 'No Stream'})"
                    )
                else:
                    print(
                        f"Batch {batch_name_label} ({stream if stream else 'No Stream'}) already exists."
                    )

        db.commit()

    def CreateStudentTable(self) -> None:
        pass

    def Create(self) -> None:
        print("Starting Database Seeding...")
        self.CreateUser()
        self.CreateTeacher()
        self.CreateSubject()
        self.CreateBatch()
        self.CreateStudent()
        print("Seeding Complete!")

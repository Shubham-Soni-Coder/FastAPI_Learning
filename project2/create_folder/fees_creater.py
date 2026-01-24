from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models import User, Class, Student
from app.utils.json_loader import load_json
from app.models import StudentFeesDue
from app.schemas.fees import StudentFeesDueCreate

# load the student data
JSON_DATA = load_json("data.json")
JSON_DATA = JSON_DATA["students"]

# store in database
Base.metadata.create_all(bind=engine)

# make a db
db = SessionLocal()


def create_fees():
    """
    Create fees for all students
    """
    class_id = 11
    ids = [
        row[0]
        for row in db.query(Student.id).filter(Student.class_id == class_id).all()
    ]
    for i in range(3, 13):
        for id in ids:
            schems = StudentFeesDueCreate(
                student_id=id,
                month=i,
                year=2025,
                total_amount=4000,
                status="pending",
            )
            model = StudentFeesDue(**schems.model_dump())
            db.add(model)

    db.commit()

from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import Class, User
from app.utils.json_loader import load_json
from app.schemas.classes import ClassCreate

# load the student data
JSON_DATA = load_json()
JSON_DATA = JSON_DATA["teacher_classes"]


# store in database
# Base.metadata.create_all(bind=engine)

# make a db
db = SessionLocal()


def add_data_classes(JSON_DATA):
    # first get the teacher_id
    teacher_id = [
        id[0] for id in db.query(User.id).filter(User.role == "Teacher").all()
    ]

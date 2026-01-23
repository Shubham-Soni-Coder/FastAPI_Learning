from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import User
from app.schemas import UserCreate
from app.core.security import hash_password

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


if __name__ == "__main__":
    user_create()

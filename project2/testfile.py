from app.database import engine, Base, get_db, session
from app.models import Base, User


# def verify_password(password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(password, hashed_password)


# store in database
Base.metadata.create_all(bind=engine)

db = session()


def show_data():
    data = db.query(User).all()
    for i, user in enumerate(data):
        print(i, user.username, user.gmail_id, user.password, user.created_at)
    db.close()


if __name__ == "__main__":
    show_data()

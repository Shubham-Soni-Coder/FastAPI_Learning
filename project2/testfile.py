from app.database import engine, Base, get_db, session
from app.models import Base, User


# store in database
Base.metadata.create_all(bind=engine)

db = session()


def show_data():
    data = db.query(User).all()
    for i, user in enumerate(data):
        print(i, user.gmail_id, user.otp_hash, user.expires_at)
    db.close()


if __name__ == "__main__":
    show_data()

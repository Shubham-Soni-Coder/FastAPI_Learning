from sqlalchemy.orm import Session
from datetime import datetime
from app.models import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import CustomException
from app.schemas import UserCreate


from app.services.otp_service import send_otp, verify_otp


def start_register(db: Session, gmail: str, password: str, session: dict):
    if db.query(User).filter(User.gmail_id == gmail).first():
        raise CustomException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    send_otp(gmail, db)

    session["gmail"] = gmail
    session["password"] = hashed_password
    session["time"] = datetime.utcnow()


def complet_register(db: Session, session: dict, otp: str):
    gmail = session.get("gmail")
    password = session.get("password")

    if not gmail or not password:
        raise CustomException(status_code=400, detail="Invalid session")

    if not verify_otp(gmail, otp, db):
        raise CustomException(status_code=400, detail="Invalid OTP")

    schems = UserCreate(gmail=gmail, password=hash_password(password))
    user = User(**schems.dict())
    db.add(user)
    db.commit()


def login_user(db: Session, gmail: str, password: str, session: dict):
    user = db.query(User).filter(User.gmail == gmail).first()
    if not user:
        raise CustomException(status_code=400, detail="User not found")
    if not verify_password(password, user.password):
        raise CustomException(status_code=400, detail="Invalid password")
    session["gmail"] = user.gmail

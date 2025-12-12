from dotenv import load_dotenv
import os
import string
import secrets
import resend
from datetime import datetime, timedelta
import hashlib
from models import OTP
from database import engine, Base, get_db, session


load_dotenv()
resend_api_key = os.getenv("RESEND_API_KEY")

resend.api_key = resend_api_key

if not resend_api_key:
    raise "Plz add resend api key from resend website"

# store in database
Base.metadata.create_all(bind=engine)

db = session()


def generate_otp(length=4) -> str:
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(length))


def delete_data():
    db.query(OTP).delete()
    db.commit()
    db.close()


def send_otp(email: str) -> None:
    otp = generate_otp()

    resend.Emails.send(
        {
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": "Your OTP is here!",
            "html": f"<p>Your OTP is: <strong>{otp}</strong></p>",
        }
    )
    store_otp(email, otp)
    return otp


def store_otp(email: str, otp: str) -> None:
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    expires_at = datetime.now() + timedelta(minutes=5)
    db_otp = OTP(gmail_id=email, otp_hash=otp_hash, expires_at=expires_at)
    db.add(db_otp)
    db.commit()
    print("User registered successfully")
    db.close()


def show_data():
    data = db.query(OTP).all()
    for i, user in enumerate(data):
        print(i, user.gmail_id, user.otp_hash, user.expires_at)


def check_otp(email: str, otp: str) -> bool:
    stored_otp = (
        db.query(OTP).filter(OTP.gmail_id == email).order_by(OTP.id.desc()).first()
    )

    if not stored_otp:
        return False

    if datetime.now() > stored_otp.expires_at:
        return False

    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    return otp_hash == stored_otp.otp_hash


if __name__ == "__main__":
    send_otp("sonishubham2888@gmail.com")
    user_otp = input("Enter your otp : ")
    user_otp = str(user_otp)
    print(check_otp("sonishubham2888@gmail.com", user_otp))

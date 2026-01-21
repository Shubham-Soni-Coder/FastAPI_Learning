import string
import secrets
import resend
import hashlib
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import OTP
from app.core.config import Settings

# Initialize Resend with API key from settings
resend.api_key = Settings.RESEND_API_KEY


def generate_otp(length=6) -> str:
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(length))


def send_otp(email: str, db: Session) -> str:
    otp = generate_otp(length=6)

    try:
        resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": email,
                "subject": "Your OTP is here!",
                "html": f"<p>Your OTP is: <strong>{otp}</strong></p>",
            }
        )
    except Exception as e:
        print(f"Error sending email: {e}")
        # In production you might want to raise an exception or handle this gracefully

    store_otp(db, email, otp)
    return otp


def store_otp(db: Session, email: str, otp: str) -> None:
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    db_otp = OTP(gmail_id=email, otp_hash=otp_hash, expires_at=expires_at)
    db.add(db_otp)
    db.commit()


def verify_otp(email: str, otp: str, db: Session) -> bool:
    stored_otp = (
        db.query(OTP).filter(OTP.gmail_id == email).order_by(OTP.id.desc()).first()
    )

    if not stored_otp:
        return False

    if datetime.utcnow() > stored_otp.expires_at:
        return False

    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    return otp_hash == stored_otp.otp_hash


def delete_all_otps(db: Session):
    db.query(OTP).delete()
    db.commit()

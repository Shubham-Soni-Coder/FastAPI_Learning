from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True, index=True, nullable=False)
    gmail_id = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(20), nullable=False)  # use pydamtic for range
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(50), index=True, nullable=False)
    otp_hash = Column(String(120), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

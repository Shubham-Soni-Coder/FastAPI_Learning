from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.base import Base
from datetime import datetime


class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(50), index=True, nullable=False)
    otp_hash = Column(String(120), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

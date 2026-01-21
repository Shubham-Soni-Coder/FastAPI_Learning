from pydantic import BaseModel
from datetime import datetime


class OTP(BaseModel):
    gmail_id: str
    otp_hash: str
    expires_at: datetime

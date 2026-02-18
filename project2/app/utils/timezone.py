from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def now_ist():
    """Return Current time in IST time zone"""
    return datetime.now(IST)

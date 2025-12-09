from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    Username = Column(String(15), unique=True, index=True, nullable=False)
    gmail_id = Column(String(30), unique=True, index=True, nullable=False)
    password = Column(String(20), nullable=False)  # use pydamtic for range
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

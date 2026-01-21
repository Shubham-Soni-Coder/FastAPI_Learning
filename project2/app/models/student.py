from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(Integer, nullable=True)
    name = Column(String(50), nullable=False)
    father_name = Column(String(30), nullable=False)
    mother_name = Column(String(30), nullable=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(500), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    is_active = Column(Boolean, default=False)
    class_ = relationship("Class", backref="students")

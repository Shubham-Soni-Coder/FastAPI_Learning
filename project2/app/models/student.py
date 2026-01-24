from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    roll_no = Column(Integer, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    class_ = relationship("Class", backref="students")
    User_ = relationship("User")

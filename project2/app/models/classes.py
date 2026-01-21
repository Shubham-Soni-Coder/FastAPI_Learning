from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(50), nullable=False)
    stream = Column(String(10), nullable=True)

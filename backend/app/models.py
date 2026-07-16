from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    level = Column(String, default="easy")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    level = Column(String, nullable=False)
    expected = Column(JSON, nullable=False)  # {"grossProfit": 20000, "netIncome": 10000}
    created_at = Column(DateTime, default=datetime.utcnow)
    submissions = relationship("Submission", back_populates="case")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    score = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)
    feedback = Column(JSON, nullable=True)   # Will store AI feedback + details
    completed_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="submissions")
    case = relationship("Case", back_populates="submissions")
# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Specialty(Base):
    __tablename__ = "specialties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), nullable=False)
    specialty = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")
    conversation_id = Column(String(100), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

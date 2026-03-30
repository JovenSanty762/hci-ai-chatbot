# backend/app/routes/appointments.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Appointment

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("/")
def list_appointments(db: Session = Depends(get_db)):
    """Endpoint para supervisión humana (ISO 42001 - Involucramiento Humano)"""
    return db.query(Appointment).all()

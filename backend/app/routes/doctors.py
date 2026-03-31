from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Doctor, Specialty
from ..schemas.doctor import DoctorCreate, DoctorResponse, SpecialtyResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/specialties/", response_model=List[SpecialtyResponse])
def get_specialties(db: Session = Depends(get_db)):
    return db.query(Specialty).all()

@router.get("/", response_model=List[DoctorResponse])
def get_doctors(specialty_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Doctor)
    if specialty_id:
        query = query.filter(Doctor.specialty_id == specialty_id)
    return query.filter(Doctor.is_active == True).all()

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return doctor

from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional
from ..models import Gender   # Importamos el Enum del models.py

class PatientBase(BaseModel):
    cedula: str = Field(..., min_length=5, max_length=20, example="123456789")
    nombre_completo: str = Field(..., min_length=3, max_length=120)
    telefono: str = Field(..., min_length=7, max_length=15, example="3101234567")
    email: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[Gender] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True   # Reemplaza orm_mode en Pydantic v2

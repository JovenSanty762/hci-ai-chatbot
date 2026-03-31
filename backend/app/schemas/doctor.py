from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import time

class SpecialtyBase(BaseModel):
    nombre: str = Field(..., max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)

class SpecialtyResponse(SpecialtyBase):
    id: int

    class Config:
        from_attributes = True

class DoctorBase(BaseModel):
    nombre_completo: str = Field(..., max_length=120)
    telefono: Optional[str] = Field(None, max_length=15)
    licencia: Optional[str] = Field(None, max_length=30)

class DoctorCreate(DoctorBase):
    specialty_id: int

class DoctorResponse(DoctorBase):
    id: int
    specialty: SpecialtyResponse
    is_active: bool

    class Config:
        from_attributes = True

class DoctorAvailabilityBase(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)   # 0=lunes, 6=domingo
    start_time: time
    end_time: time

class DoctorAvailabilityResponse(BaseModel):
    id: int
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

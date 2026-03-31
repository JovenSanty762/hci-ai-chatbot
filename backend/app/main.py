# backend/app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Patient, Specialty, Doctor, DoctorAvailability, Appointment
from .routes import chatbot, appointments
from .database import engine, Base
from .models import *          # Para que cree todas las tablas
from .routes.patients import router as patients_router
from .routes.doctors import router as doctors_router
from .routes.availability import router as availability_router
from .routes.appointments import router as appointments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HCI AI Chatbot - Agendamiento de Citas Médicas",
    description="Backend para chatbot de citas médicas",
    version="1.0.0"
)

# CORS para frontend
# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)

        logger.info(
            f"{request.method} {request.url.path} | Status={response.status_code} | {duration}s"
        )
        return response

    except Exception as e:
        duration = round(time.time() - start_time, 4)
        logger.error(
            f"ERROR en {request.method} {request.url.path} | {duration}s | {str(e)}"
        )
        logger.error(traceback.format_exc())

        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )

# Rutas
app.include_router(chatbot.router)
app.include_router(doctors_router)
app.include_router(patients_router)
app.include_router(availability_router)
app.include_router(appointments_router)

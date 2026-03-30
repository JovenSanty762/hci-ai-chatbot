# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chatbot, appointments
from .database import engine, Base
import uvicorn

app = FastAPI(
    title="HCI-IA-Chatbot API",
    description="API del Chatbot de Agendamiento con IA - Alineado con ISO 42001",
    version="1.0.0"
)

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción limitar a dominio interno
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas en MySQL
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(chatbot.router)
app.include_router(appointments.router)

@app.get("/health")
async def health_check():
    """Endpoint para monitoreo y auditoría ISO 42001"""
    return {"status": "healthy", "system": "hci-ia-chatbot", "compliance": "ISO 42001"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

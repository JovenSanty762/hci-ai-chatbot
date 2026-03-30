# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chatbot, appointments
from .database import engine, Base
import uvicorn

app = FastAPI(title="Hospital AI ChatBot")

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

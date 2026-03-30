from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from .config import DATABASE_URL
from .logger import logger

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    logger.info("Conexión a MySQL inicializada correctamente.")

except SQLAlchemyError as e:
    logger.error(f"Error inicializando conexión a MySQL: {str(e)}")
    raise

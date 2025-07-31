from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

# Set up logging for debugging database
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load database URL from settings (.env file)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

# Create a session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
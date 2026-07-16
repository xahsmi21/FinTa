from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path
# Get the folder where this file (database.py) is located
BASE_DIR = Path(__file__).parent.parent  # goes up to 'backend/'

# Load .env from that folder
env_path = BASE_DIR / ".env"

load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLite requires special connect_args for async support
# But we'll use sync SQLAlchemy for simplicity with SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
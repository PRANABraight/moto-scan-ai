from sqlmodel import Session, SQLModel, create_engine
from pathlib import Path
import os

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Create database directory if it doesn't exist
db_dir = BASE_DIR / "data"
db_dir.mkdir(exist_ok=True)

# SQLite database URL
DATABASE_URL = f"sqlite:///{db_dir}/database.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

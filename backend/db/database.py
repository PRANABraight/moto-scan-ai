# backend/db/database.py

from sqlmodel import create_engine, Session, SQLModel # <-- FIX: SQLModel was missing

# This path assumes the database file is in the 'backend' directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False) # Set echo to False for cleaner logs

def create_db_and_tables():
    # This line needs the SQLModel import to work
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
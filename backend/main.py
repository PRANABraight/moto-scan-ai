from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import create_db_and_tables
from app.api.v1.endpoints import damage_detection # Assuming you have an __init__.py in endpoints

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if your frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(damage_detection.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
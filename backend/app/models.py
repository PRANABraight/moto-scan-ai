from datetime import datetime
from typing import List, Optional, Dict
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password_hash: str
    first_name: str
    last_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DamageAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    image_path: str
    damage_detected: bool
    confidence: float
    severity: str
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    analysis_data: Dict = Field(default={})

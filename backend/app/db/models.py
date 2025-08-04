from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import Field, SQLModel, JSON

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DamageAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    image_uri: str
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    damage_detected: bool
    damage_types: Dict = Field(default={}, sa_type=JSON)
    severity: str
    cost_estimation: Dict = Field(default={}, sa_type=JSON)
    status: str = Field(index=True)
    confidence: float

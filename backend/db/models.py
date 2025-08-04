from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Coordinates(BaseModel):
    x: int
    y: int
    width: int
    height: int

class DamageType(BaseModel):
    type: str
    location: str
    severity: str
    coordinates: Coordinates

class CostBreakdown(BaseModel):
    item: str
    cost: float
    description: str

class CostEstimation(BaseModel):
    total_cost: float
    labor_cost: float
    parts_cost: float
    paint_cost: float
    breakdown: List[CostBreakdown]

class DamageAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    image_uri: str
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    damage_detected: bool
    damage_types: List[DamageType]
    severity: str
    cost_estimation: CostEstimation
    status: str = Field(index=True)
    confidence: float

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
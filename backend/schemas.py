from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_url: Optional[str] = None
    order_index: int = 0
    is_mandatory: bool = True

class CourseCreate(CourseBase):
    specialization_id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    order_index: Optional[int] = None
    is_mandatory: Optional[bool] = None

class Course(CourseBase):
    id: int
    specialization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Specialization schemas
class SpecializationBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_months: Optional[int] = None
    prerequisites: Optional[str] = None

class SpecializationCreate(SpecializationBase):
    pass

class SpecializationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_months: Optional[int] = None
    prerequisites: Optional[str] = None
    is_active: Optional[bool] = None

class Specialization(SpecializationBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    courses: List[Course] = []
    
    class Config:
        from_attributes = True

class SpecializationWithUsers(Specialization):
    users: List[User] = []

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
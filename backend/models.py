from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# SQLAlchemy User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    token = Column(String, nullable=True)  # Store token for ESP32 and Flutter auto-auth


# Pydantic models
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True  # For Pydantic v2 (was orm_mode in v1)

class Token(BaseModel):
    access_token: str
    token_type: str

from datetime import datetime
from config.database import Base
from pydantic import BaseModel, EmailStr, ConfigDict, UUID4
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str

class UserLogin(BaseModel):
    phone_number: str

class UserOtp(BaseModel):
    phone_number: str
    otp: str



class UserResponse(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    phone_number: str
    is_verified: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone_number: str

class Config:
        orm_mode = True
        from_attributes = True

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)



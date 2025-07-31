from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8)

    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one uppercase letter and one digit")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class UserInDB(UserOut):
    hashed_password: str
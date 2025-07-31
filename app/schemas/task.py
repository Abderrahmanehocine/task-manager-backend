from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: bool = False

class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None

class TaskOut(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    due_date: Optional[datetime]

    class Config:
        orm_mode = True
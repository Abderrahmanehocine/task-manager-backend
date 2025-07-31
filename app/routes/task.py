from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.crud.task import create_task, get_tasks_by_user, get_task, update_task, delete_task
from app.models.user_model import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter()

@router.post("/", response_model=TaskOut)
async def create_task_route(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new task for the authenticated user."""
    return create_task(db, task, current_user)

@router.get("/", response_model=List[TaskOut])
async def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all tasks for the authenticated user."""
    return get_tasks_by_user(db, current_user.id)

@router.get("/{task_id}", response_model=TaskOut)
async def get_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific task by ID."""
    task = get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
async def update_task_route(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update a task by ID."""
    updated_task = update_task(db, task_id, task, current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
async def delete_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a task by ID."""
    if not delete_task(db, task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
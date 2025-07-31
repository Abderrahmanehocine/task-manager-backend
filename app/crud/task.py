from sqlalchemy.orm import Session
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task import TaskCreate, TaskUpdate

def create_task(db: Session, task: TaskCreate, user: User) -> Task:
    """Create a new task for the authenticated user."""
    db_task = Task(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        due_date=task.due_date,
        user_id=user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, user_id: int) -> list[Task]:
    """Get all tasks for a user."""
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(db: Session, task_id: int, user_id: int) -> Task | None:
    """Get a task by ID, ensuring it belongs to the user."""
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Task | None:
    """Update a task by ID, ensuring it belongs to the user."""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """Delete a task by ID, ensuring it belongs to the user."""
    task = get_task(db, task_id, user_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user import UserCreate
from app.core.password import hash_password

def get_user_by_username(db: Session, username: str) -> User | None:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user with hashed password."""
    if get_user_by_username(db, user.username):
        raise ValueError("Username already taken")
    if get_user_by_email(db, user.email):
        raise ValueError("Email already taken")
    
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
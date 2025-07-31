from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.password import verify_password
from app.crud.user import create_user, get_user_by_username
from app.models.user_model import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user with hashed password."""
    try:
        db_user = create_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
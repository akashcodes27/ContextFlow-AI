from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_service import (
    create_user,
    authenticate_user
)
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# REGISTER
# -------------------------
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = authenticate_user(db, user.email, user.password)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = create_user(
        db,
        email=user.email,
        password=user.password,
        full_name=user.full_name
    )

    return new_user


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
# ME (protected route)
# -------------------------
@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user
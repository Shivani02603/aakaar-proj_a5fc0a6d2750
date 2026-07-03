backend/routers/auth.py
```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.config import get_db
from backend.schemas import UserCreate
from backend.services.auth import create_user, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/api/auth/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User registered successfully"}

@router.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user.id, "token_type": "bearer"}
```
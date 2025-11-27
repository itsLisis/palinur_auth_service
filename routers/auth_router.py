from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
import models, schemas

from security.hashing import Hash
from security import jwt_handler

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # Verify if email is already registered
    user_exists = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_pw = Hash.hash_password(user_data.password)

    # Create new user
    new_user = models.User(
        email=user_data.email,
        birthday=user_data.birthday,
        hashed_password=hashed_pw,
        completed_profile=False
    )

    # Safe in the DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Optional: generate JTW token
    # token = create_access_token({"user_id": new_user.id})

    # returning user (id, completed_profile, email, birthday )
    return new_user

@router.post("/login", response_model=schemas.TokenResponde)
def login_user(
    user_login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    
    # Verify if email exists
    user = db.query(models.User).filter(models.User.email == user_login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Email is not registered"
        )
    
    # Verify password
    valid_password = Hash.verify_password(
        user_login_data.password,
        user.hashed_password
    )
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )
    
    #  If everything is correct -> generate JWT
    token = jwt_handler.create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
import models, schemas

from security.hashing import Hash
from security import jwt_handler

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.TokenResponde)
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
        hashed_password=hashed_pw,
        completed_profile=False
    )

    # Safe in the DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token for automatic login after registration
    token = jwt_handler.create_access_token({
        "user_id": new_user.id,
        "complete_profile": False
    })

    # Return token and user info (profile is always incomplete after registration)
    return {
        "access_token": token,
        "token_type": "bearer",
        "complete_profile": False,
        "user_id": new_user.id
    }

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
    token = jwt_handler.create_access_token({
        "user_id": user.id,
        "complete_profile": user.completed_profile
    })

    return {
        "access_token": token, 
        "token_type": "bearer",
        "complete_profile": user.completed_profile,
        "user_id": user.id
    }

@router.patch("/users/{user_id}/complete_profile", response_model=schemas.TokenResponde)
def mark_profile_complete(
    user_id: int,
    db: Session = Depends(get_db)
):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Actualizar el estado del perfil
    user.completed_profile = True
    db.commit()
    db.refresh(user)
    
    token = jwt_handler.create_access_token({
        "user_id": user.id,
        "complete_profile": True
    })
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "complete_profile": True,
        "user_id": user.id
    }
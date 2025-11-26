from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
import models, schemas

from security.hashing import Hash

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # 1. Verify if email is already registered
    user_exists = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hash password
    hashed_pw = Hash.hash_password(user_data.password)

    # 3. Create new user
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

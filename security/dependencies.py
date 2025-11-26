from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from db import get_db
from models import User
from security.jwt_handler import decode_access_token

bearer_scheme = HTTPBearer()

def get_current_user(
    token: str = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    decoded = decode_access_token(token.credentials)

    if decoded is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = decoded.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

"""
@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return current_user
"""
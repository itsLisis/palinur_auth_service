from pydantic import BaseModel, EmailStr
from datetime import date

# Base schema
class UserBase(BaseModel):
    email: EmailStr
    birthday: date

# Schema used for creating users
class UserCreate(UserBase):
    password: str

# Schema used for returning users to the client
class UserResponse(UserBase):
    id: int
    completed_profile: bool

    class Config:
        from_attributes = True
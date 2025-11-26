from pydantic import BaseModel, EmailStr
from datetime import date

# Base schema
class UserBase(BaseModel):
    email: EmailStr
    birthday: date

# Schema used for creating users
class UserCreate(UserBase):
    password: str # The password here is in plain text because is the user input
                    # we need to hash the password and safe it in the db

# Schema used for returning users to the client - Think we are not going to use this
class UserResponse(UserBase):
    id: int
    completed_profile: bool

    class Config:
        from_attributes = True
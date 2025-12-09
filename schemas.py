from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    turnstile_token: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    turnstile_token: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    completed_profile: bool

    class Config:
        from_attributes = True

class TokenResponde(BaseModel):
    access_token: str
    token_type: str
    complete_profile: bool
    user_id: int
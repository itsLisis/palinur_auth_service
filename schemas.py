from pydantic import BaseModel, EmailStr, field_validator
import re

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    turnstile_token: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

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
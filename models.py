from sqlalchemy import Column, Integer, String, Date
from db import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth_service"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    birthday = Column(Date, nullable=False)
    hashed_password = Column(String, nullable=False)
from sqlalchemy import Column, Integer, String, Boolean
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String)
    completed_profile = Column(Boolean, default=False)

"""
# User service
class Profile(Base):

    __tablename__ = "profiles"
    __table_args__ = {"schema": "user_service"}

    introduction = Column(String, nullable=False)
    name = Column(String, nullable=False)
    sexual_orientation = Column(String, nullable=False)

"""
from fastapi import FastAPI
from db import Base, engine
import models
from routers import auth_router, users_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
#app.include_router(users_router)
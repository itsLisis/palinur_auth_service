from fastapi import FastAPI
from db import Base, engine
from routers import auth_router, users_router

app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)

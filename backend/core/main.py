from fastapi import FastAPI
from .routes.router import router
from .database import Base, engine

app = FastAPI(title="My To Do List")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(router)

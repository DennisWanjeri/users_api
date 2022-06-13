from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import requests
from .database import engine
from . import models
from .schemas import PostModel, UpdatedPost
from sqlalchemy.orm import Session
from . database import get_db
from .routers import posts, users
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

posts_url = "https://jsonplaceholder.typicode.com/posts"
users_url = "https://jsonplaceholder.typicode.com/users"

app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "welcome to my api!"}

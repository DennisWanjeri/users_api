from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import requests
from .database import engine
from . import models
from .schemas import PostModel
from sqlalchemy.orm import Session
from . database import get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

posts_url = "https://jsonplaceholder.typicode.com/posts"
users_url = "https://jsonplaceholder.typicode.com/users"


@app.get("/")
def root():
    return {"message": "welcome to my api!"}


@app.get('/posts')
def get_posts():
    response = requests.get(posts_url).json()
    return response


@app.get('/posts/{id}')
def get_post_by_id(id: int):
    response = requests.get(posts_url).json()
    for item in response:
        if id == item['id']:
            return item
    return {"message": "post not found"}


@app.get('/users')
def get_users():
    response = requests.get(users_url).json()
    return response


@app.post('/posts')
def add_post(post: PostModel, db: Session = Depends(get_db)):

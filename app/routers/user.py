from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import requests
from ..schemas import PostModel, UpdatedPost
from ..database import get_db
from .. import models

posts_url = "https://jsonplaceholder.typicode.com/posts"
users_url = "https://jsonplaceholder.typicode.com/users"

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/')
def get_users():
    response = requests.get(users_url).json()
    return response


@router.get('/posts/{id}')
def get_posts_by_user_id(id: int):
    all_users = requests.get(users_url).json()
    for item in all_users:
        if item['id'] == id:
            correct_user = True

    if not correct_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user of id: {id} was not found")

    response = requests.get(posts_url).json()
    posts_user = []
    for item in response:
        if item['userId'] == id:
            posts_user.append(item)
    return posts_user

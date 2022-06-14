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

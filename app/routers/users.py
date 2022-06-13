from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..main import posts_url, users_url
import requests
from ..schemas import PostModel, UpdatedPost
from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/posts",
    tags=['Users']
)


@router.get('/')
def get_users():
    response = requests.get(users_url).json()
    return response

from fastapi import FastAPI, Response, status, HTTPException, Depends
import requests
from sqlalchemy.orm import Session
from . import models
from .database import get_db


posts_url = "https://jsonplaceholder.typicode.com/posts"


def database_sync(db: Session = Depends(get_db)):
    response = requests.get(posts_url)
    for item in response:
        item_id = item['id']
        post_query = db.query(models.Post).filter(models.Post.id == item_id)
        post = post_query.first()
        if not post:
            new_post = models.Post(**item.dict())
            db.add(new_post)
            db.commit()

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import requests
from ..schemas import PostModel, UpdatedPost
from ..database import get_db
from .. import models

posts_url = "https://jsonplaceholder.typicode.com/posts"
users_url = "https://jsonplaceholder.typicode.com/users"

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# verify if the record exists in the database
# if it doesnt exist post it into the database


@router.get('/')
def database_sync(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    response = requests.get(posts_url).json()
    for item in response:
        item_id = item['id']
        post_query = db.query(models.Post).filter(models.Post.id == item_id)
        post = post_query.first()
        if not post:
            new_post = models.Post(
                id=item['id'], userId=item['userId'], title=item['title'], body=item['body'])
            db.add(new_post)
            db.commit()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/{id}')
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        response = requests.get(posts_url).json()
        for item in response:
            if item['id'] == id:
                post = item
                print(item)
                new_post = models.Post(
                    id=item['id'], userId=item['userId'], body=item['body'], title=item['title'])
                db.add(new_post)
                db.commit()
                db.refresh(new_post)
                return new_post
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@router.post('/')
def add_post(post: PostModel, db: Session = Depends(get_db)):
    all_users = requests.get(users_url).json()
    correct_user = False
    for item in all_users:
        if item['id'] == post.userId:
            correct_user = True

    if not correct_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user of id: {post.userId} was not found")
    obj = db.query(models.Post).order_by(models.Post.id.desc()).first()
    last_id = obj.id + 1
    new_post = models.Post(id=last_id,
                           userId=post.userId, body=post.body, title=post.title)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{id}')
def update_post(id: int, updated_post: UpdatedPost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_f = post_query.first()
    if not post_f:
        all_posts = requests.get(posts_url).json()
        for item in all_posts:
            if item['id'] == id:
                post_f = item
                new_post = models.Post(
                    userId=updated_post.userId, body=updated_post.body, title=updated_post.title)
                db.add(new_post)
                db.commit()
                db.refresh(new_post)
                return new_post
    if not post_f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post of id: {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_f = post_query.first()
    if post_f:
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    all_posts = requests.get(posts_url).json()
    for item in all_posts:
        if item['id'] == id:
            requests.delete(f"{posts_url}/{id}")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

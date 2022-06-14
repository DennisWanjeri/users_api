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


@router.get('/')
def get_posts():
    response = requests.get(posts_url).json()
    return response


@router.get('/{id}')
def get_post_by_id(id: int):
    response = requests.get(posts_url).json()
    for item in response:
        if id == item['id']:
            return item
    return {"message": "post not found"}


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

    new_post = models.Post(**post.dict())
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

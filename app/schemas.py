from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostModel(BaseModel):
    title: str
    body: str
    userId: int


class UpdatedPost(PostModel):
    pass

from pydantic import BaseModel 

class PostCreate(BaseModel):
    title: str
    content: str


class PostRespone(BaseModel):
    title: str
    content: str
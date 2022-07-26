from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    class Config:
        orm_mode = True

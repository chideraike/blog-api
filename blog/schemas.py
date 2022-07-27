from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(BlogBase):
    creator: ShowUser

    class Config:
        orm_mode = True

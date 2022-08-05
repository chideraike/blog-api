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


class ShowUserWithoutBlogs(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowBlog(BlogBase):
    creator: ShowUser

    class Config:
        orm_mode = True


class ShowBlogs(BlogBase):
    creator: ShowUserWithoutBlogs

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

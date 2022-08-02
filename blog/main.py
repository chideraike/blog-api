from fastapi import FastAPI

from . import models
from .database import engine
from .routers import blog, user, auth

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)

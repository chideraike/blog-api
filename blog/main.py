from fastapi import FastAPI
from . import schemas, models
from .database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.post("/blog")
def create(request: schemas.Blog):
    return request

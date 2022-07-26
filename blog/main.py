from fastapi import FastAPI
from .schemas import Blog

app = FastAPI()


@app.post("/blog")
def create(request: Blog):
    return request

import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/blog")
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # Only get 10 published blogs
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "unpublished blog"}


@app.get("/blog/{id}")
def show(id: int):
    # fetch blog with id = id
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id, limit=10):
    # fetch comments of blog with id = id
    return {
        "data": [
            {"1": "comment 1"},
        ]
    }


class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with title as {blog.title}"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)

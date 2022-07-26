from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal
from .hashing import Hash

models.Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_a_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", tags=["Blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["Blogs"],
)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}

    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update_a_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    blog.title = request.title
    blog.body = request.body
    db.commit()
    return {"detail": "Blog updated successfully"}


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete_blog_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/user",
    response_model=schemas.ShowUser,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get(
    "/user/{id}",
    response_model=schemas.ShowUser,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    return user

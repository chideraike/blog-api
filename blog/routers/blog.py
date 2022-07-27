from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models

router = APIRouter()
get_db = database.get_db


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get("/blog", response_model=list[schemas.ShowBlog], tags=["Blogs"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@router.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["Blogs"],
)
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    return blog


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    blog.title = request.title
    blog.body = request.body
    db.commit()

    return {"detail": "Blog updated successfully"}


@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    db.delete(blog)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

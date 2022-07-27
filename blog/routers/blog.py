from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models

router = APIRouter(prefix="/blog", tags=["Blogs"])
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get("/", response_model=list[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
)
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    return blog


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    db.delete(blog)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import blog

router = APIRouter(prefix="/blog", tags=["Blogs"])
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.get("/", response_model=list[schemas.ShowBlogs])
def get_blogs(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlogs,
)
def get_blog(id: int, db: Session = Depends(get_db)):
    return blog.get(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog.delete(id, db)

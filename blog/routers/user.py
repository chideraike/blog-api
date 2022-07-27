from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, hashing

router = APIRouter()
get_db = database.get_db
Hash = hashing.Hash


@router.post(
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


@router.get(
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

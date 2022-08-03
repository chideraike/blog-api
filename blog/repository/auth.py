from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, hashing

Hash = hashing.Hash


def login(request: schemas.Login, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Incorrect email or password",
        )

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Incorrect email or password",
        )

    # Generate a jwt token and return it
    return user

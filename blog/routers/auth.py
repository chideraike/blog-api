from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import auth

router = APIRouter(prefix="/auth", tags=["Authentication"])
get_db = database.get_db


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth.login(request, db)

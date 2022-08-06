from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import auth

router = APIRouter(prefix="/auth", tags=["Authentication"])
get_db = database.get_db


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return auth.login(request, db)

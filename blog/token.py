from datetime import datetime, timedelta
from jose import JWTError, jwt
from .schemas import TokenData

SECRET_KEY = "b63b7242b8e53321ca26dfdb46b18154fc9279b7157eb82897840d52770d9689"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

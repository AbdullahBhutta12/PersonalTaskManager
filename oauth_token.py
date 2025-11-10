from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

import schemas

SECRET_KEY = "660b877141ae764a79ea7fda2f4e3995eb4110c8b17cf9a18af731db8afe603d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=email, id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data

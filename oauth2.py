from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.exc import InvalidTokenError
from sqlalchemy.orm import Session

from oauth_token import SECRET_KEY, ALGORITHM, verify_token
import database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        from jose import jwt
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.query(models.User).filter(username == models.User.email).first()
    if user is None:
        raise credentials_exception
    return user

    # return verify_token(token, credentials_exception)

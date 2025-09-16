from fastapi import APIRouter, Depends, status, HTTPException
import models, oauth_token, database
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(request.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    if Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")

    access_token = oauth_token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

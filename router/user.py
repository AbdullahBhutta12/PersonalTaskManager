from typing import List

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

import schemas, database, oauth2
from repository import user

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/sign_up', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(username: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            profile_image: UploadFile = File(...),
            db: Session = Depends(database.get_db)):
    return user.create(username, email, password, profile_image, db)

#
# @router.get('/logout', response_model=schemas.UserResponse)
# def get_user(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return user.get_user(db, current_user)
#
#
# @router.get('/', response_model=List[schemas.UserResponse])
# def users(db: Session = Depends(database.get_db)):
#     return user.users(db)

from typing import List

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

import schemas, database
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
# @router.get('/{user_id}', response_model=schemas.UserResponse)
# def get_user(user_id: int, db: Session = Depends(database.get_db)):
#     return user.get_user(user_id, db)
#
#
# @router.get('/', response_model=List[schemas.UserResponse])
# def users(db: Session = Depends(database.get_db)):
#     return user.users(db)

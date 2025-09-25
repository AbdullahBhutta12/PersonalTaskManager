from fastapi import APIRouter, Depends, status

import schemas, database
from repository import user

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/sign_up', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def sign_up(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    return user.get_user(user_id, db)

@router.get('/')
def users(db: Session = Depends(database.get_db)):
    return user.users(db)

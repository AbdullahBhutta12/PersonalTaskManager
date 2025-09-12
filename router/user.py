from fastapi import APIRouter, Depends

import schemas, database
from repository import user

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/create_user', response_model=schemas.ShowUser)
def create_user(request: schemas.CreateUser, db: Session = Depends(database.get_db)):
    return user.create(request, db)

@router.get('/show_users/{user_id}', response_model=schemas.ShowUser)
def show_users(db: Session = Depends(database.get_db)):
    return user.show_user(db)
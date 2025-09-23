from fastapi import APIRouter, Depends

import schemas, database
from repository import user

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/create_user', response_model=schemas.User)
def create_user(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    print("in api")
    return user.create(request, db)


@router.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    return user.get_user(user_id, db)

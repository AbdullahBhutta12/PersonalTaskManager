from fastapi import APIRouter, Depends

import schemas, database
from repository import user

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.CreateUser, db: Session = Depends(database.get_db)):
    return user.create(request, db)
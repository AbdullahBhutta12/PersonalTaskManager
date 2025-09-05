from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
from database import *
from typing import List
from repository import event

router = APIRouter(
    prefix="/events",
    tags=['Events']
)

@router.get('/', response_model=List[schemas.Event])
def get_all(db: Session = Depends(get_db)):
    return event.get_all(db)

@router.post('/create_event', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Event, db: Session= Depends(get_db)):
    return event.create(request, db)

@router.delete('/delete_event', status_code=status.HTTP_204_NO_CONTENT)
def delete(event_id: int, db: Session= Depends(get_db)):
    return event.delete(event_id, db)
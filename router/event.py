from fastapi import APIRouter, Depends, status
from typing import List

import schemas
import database
from repository import event

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/events",
    tags=['Events']
)


@router.get('/', response_model=List[schemas.Event])
def get_all(db: Session = Depends(database.get_db)):
    return event.get_all(db)


@router.post('/create_event', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Event, db: Session = Depends(database.get_db)):
    return event.create(request, db)


@router.put('/update_event/{event_id}')
def update(event_id: int, request: schemas.Event, db: Session = Depends(database.get_db)):
    return event.update(event_id, db, request)


@router.delete('/delete_event/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(event_id: int, db: Session = Depends(database.get_db)):
    return event.delete(event_id, db)

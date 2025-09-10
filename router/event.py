from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
import database
from typing import List
from repository import event

router = APIRouter(
    prefix="/events",
    tags=['Events']
)

@router.get('/', response_model=List[schemas.Event])
def get_all(db: Session = Depends(database.get_db)):
    return event.get_all(db)

@router.post('/create_event', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Event, db: Session= Depends(database.get_db)):
    return event.create(request, db)

@router.put('/update_event/{event_id}')
def updated(event_id: int, request: schemas.Event, db: Session= Depends(database.get_db)):
    return event.updated(event_id, db, request)

@router.delete('/delete_event/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(event_id: int, db: Session= Depends(database.get_db)):
    return event.delete(event_id, db)
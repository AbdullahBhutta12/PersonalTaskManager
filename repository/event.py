from fastapi import HTTPException, status

import schemas
import models

from sqlalchemy.orm import Session


def get_all(db: Session):
    events = db.query(models.Event).all()
    return events


def create(request: schemas.Event, db: Session):
    new_event = models.Event(event_name=request.event_name, location=request.location, event_date=request.event_date,
                             event_time=request.event_time, user_id=1)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


def update(event_id: int, db: Session, request: schemas.Event):
    events = db.query(models.Event).filter(event_id == models.Event.id)
    if not events.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} not found")
    events.update(
        {
            "event_name": request.event_name,
            "location": request.location,
            "event_date": request.event_date,
            "event_time": request.event_time
        }, synchronize_session=False)
    db.commit()
    # db.refresh(events)
    return "Event updated"


def delete(event_id: int, db: Session):
    deleted = db.query(models.Event).filter(event_id == models.Event.id)
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} not found")
    deleted.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

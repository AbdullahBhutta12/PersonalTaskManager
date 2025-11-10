from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import schemas
import models
from firebase import send_notification_others, send_notification


def get_all(db: Session, current_user: schemas.User):
    events = db.query(models.Event).filter(current_user.id == models.Event.user_id).all()
    return events


def create(request: schemas.EventBase, db: Session, current_user: schemas.User):
    new_event = models.Event(event_name=request.event_name, location=request.location, event_date=request.event_date,
                             event_time=request.event_time, user_id=current_user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    user_device = db.query(models.DeviceToken).filter(current_user.id == models.DeviceToken.user_id).first()
    if user_device:
        try:
            send_notification(
                title=f"New Upcoming Event: {new_event.event_name}",
                body=f"At: {new_event.location}  On: {new_event.event_date}",
                token=user_device.token
            )
        except Exception as e:
            print("Notification Error", e)

    return new_event


def update(event_id: int, db: Session, request: schemas.EventBase):
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
    return "Event updated"


def delete(event_id: int, db: Session):
    deleted = db.query(models.Event).filter(event_id == models.Event.id)
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} not found")
    deleted.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, oauth2, database

from firebase import send_notification, send_notification_others

router = APIRouter(
    prefix="/notification",
    tags=["Notifications"]
)

@router.get('/send-notification')
def notification(title: str, body: str, token: str):
    response = send_notification(token, title, body)
    return {"message": "Notification sent", "response": response}

@router.get('/send-notification-others')
def notification(body: str, title: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    response = send_notification_others(db, title, body, current_user.id)
    return {"message": "Notification sent", "response": response}
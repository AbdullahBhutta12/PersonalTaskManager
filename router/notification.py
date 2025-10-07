from fastapi import APIRouter, status
from firebase import send_notification

router = APIRouter(
    prefix="/notification",
    tags=["Notifications"]
)

@router.get('/send_notification')
def notification(title: str, body: str, token: str):
    response = send_notification(token, title, body)
    return {"message": "Notification sent", "response": response}

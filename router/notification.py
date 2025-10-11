from fastapi import APIRouter
from firebase import send_notification

router = APIRouter(
    prefix="/notification",
    tags=["Notifications"]
)

@router.get('/send-notification')
def notification(title: str, body: str, token: str):
    response = send_notification(token, title, body)
    return {"message": "Notification sent", "response": response}

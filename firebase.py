

import firebase_admin
from firebase_admin import credentials, messaging
import models

if not firebase_admin._apps:
    cred = credentials.Certificate("/home/abdullah-saeed/PycharmProjects/PersonalTaskManager/firebase-key.json")
    firebase_admin.initialize_app(cred)

def send_notification(token: str, title: str, body: str):
    message = messaging.Message(
        notification = messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )

    response = messaging.send(message)
    return {"status": "success", "message_id": response}

def send_notification_others(db, title: str, body: str, current_user: int):
    user_device = db.query(models.DeviceToken.token).filter(current_user != models.DeviceToken.user_id).order_by(models.DeviceToken.created_at.desc()).all()
    print(user_device)
    user_device = [t[0] for t in user_device]
    message = messaging.MulticastMessage(
        notification = messaging.Notification(
            title=title,
            body=body
        ),
        tokens=user_device
    )

    response = messaging.send_each_for_multicast(message)
    return {"status": "success", "message_id": response}

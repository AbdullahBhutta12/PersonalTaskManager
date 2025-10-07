import firebase_admin
from firebase_admin import credentials, messaging

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


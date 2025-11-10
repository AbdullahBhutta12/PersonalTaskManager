from sqlalchemy.orm import Session
import models


def save_token(db: Session, user_id: int, token: str, ):
    existing = db.query(models.DeviceToken).filter(token == models.DeviceToken.token).first()
    if existing:
        existing.user_id = user_id
        db.add(existing)
        db.commit()
        return existing

    new = models.DeviceToken(user_id=user_id, token=token)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

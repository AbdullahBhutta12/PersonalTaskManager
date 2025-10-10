from sqlalchemy.orm import Session
import models


def save_token(db:Session, user_id:int, token: str, platform: str | None = None):
    existing = db.query(models.DeviceToken).filter(token == models.DeviceToken.token).first()
    if existing:
        existing.user_id = user_id
        existing.platform = platform
        db.add(existing)
        db.commit()
        return existing

    new = models.DeviceToken(user_id = user_id, token = token, platform = platform)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


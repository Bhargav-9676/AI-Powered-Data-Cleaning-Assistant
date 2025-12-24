from sqlalchemy.orm import Session
from app.models import ActivityLog


def log_activity(
    db: Session,
    user_email: str,
    action: str,
    description: str = None
):
    log = ActivityLog(
        user_email=user_email,
        action=action,
        description=description
    )
    db.add(log)
    db.commit()

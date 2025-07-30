from sqlalchemy.orm import Session

from ..models.log import Log


def create_log(db: Session, user_id: int | None, action: str, meta: dict | None = None):
    """Persist an application action log."""
    log = Log(user_id=user_id, action=action, meta=meta)
    db.add(log)
    db.commit() 
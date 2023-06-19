from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Logs
from schemas.models import logInput

def log_save(db: Session, log: logInput):
    db_log = Logs(timestamp=log.timestamp, message=log.message, component=log.component, loglevel=log.loglevel, transaction_id=log.transaction_id )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


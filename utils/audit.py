from models import AuditLog
from extensions import db
from flask_login import current_user
from datetime import datetime

def log_action(action, target_type=None, target_id=None):
    if not current_user.is_authenticated:
        return  # Skip logging for anonymous users

    log = AuditLog(
        user_id=current_user.id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
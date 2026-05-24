from datetime import datetime, timezone
from src.centinela.extensions import db


class SecurityEvent(db.Model):
    __tablename__ = "security_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), default="medium")
    source = db.Column(db.String(100), default="unknown")
    description = db.Column(db.Text, default="")
    details = db.Column(db.Text, default="{}")
    raw_data = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default="open")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.event_id,
            "event_type": self.event_type,
            "severity": self.severity,
            "source": self.source,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

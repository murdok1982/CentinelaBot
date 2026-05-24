from datetime import datetime, timezone
from src.centinela.extensions import db


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(100), default="unknown")
    status = db.Column(db.String(20), default="active")
    event_type = db.Column(db.String(50), default="unknown")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.alert_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "source": self.source,
            "status": self.status,
            "event_type": self.event_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }

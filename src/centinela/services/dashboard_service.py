import logging
from datetime import datetime, timezone
from src.centinela.extensions import db
from src.centinela.models.event import SecurityEvent
from src.centinela.models.alert import Alert

logger = logging.getLogger("centinela.dashboard")


class DashboardService:
    def get_summary(self) -> dict:
        total_events = SecurityEvent.query.count()
        total_alerts = Alert.query.count()
        active_alerts = Alert.query.filter_by(status="active").count()

        severity_counts = dict(
            db.session.query(Alert.severity, db.func.count())
            .group_by(Alert.severity).all()
        )
        event_type_counts = dict(
            db.session.query(SecurityEvent.event_type, db.func.count())
            .group_by(SecurityEvent.event_type).all()
        )

        security_score = self._calculate_score(active_alerts, total_events)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system_status": "operational",
            "statistics": {
                "threats_detected_today": total_events,
                "alerts_active": active_alerts,
                "alerts_total": total_alerts,
                "events_processed": total_events,
                "security_score": security_score,
            },
            "threat_distribution": event_type_counts,
            "severity_breakdown": severity_counts,
        }

    def _calculate_score(self, active_alerts: int, total_events: int) -> int:
        base = 100
        penalty = active_alerts * 5 + min(total_events // 10, 20)
        return max(base - penalty, 10)

    def is_healthy(self):
        return True

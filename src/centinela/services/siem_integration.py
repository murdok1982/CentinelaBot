import logging
import socket
import json
from datetime import datetime, timezone
from config import Config
from src.centinela.extensions import db
from src.centinela.models.event import SecurityEvent

logger = logging.getLogger("centinela.siem")


class SIEMIntegration:
    def __init__(self):
        self.syslog_socket = None
        if Config.SYSLOG_HOST:
            try:
                self.syslog_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                logger.info("Syslog forwarder configured: %s:%s", Config.SYSLOG_HOST, Config.SYSLOG_PORT)
            except Exception as e:
                logger.error("Syslog socket error: %s", e)

    def send_event(self, event_data: dict) -> dict:
        try:
            event = SecurityEvent(
                event_id=event_data.get("id", f"SIEM-{int(datetime.now().timestamp())}"),
                event_type=event_data.get("type", "unknown"),
                severity=event_data.get("severity", "medium"),
                source=event_data.get("source", "centinela"),
                description=event_data.get("description", ""),
                details=json.dumps(event_data.get("details", {})),
                status="forwarded"
            )
            db.session.add(event)
            db.session.commit()

            if self.syslog_socket:
                self._forward_to_syslog(event_data)

            logger.info("Event forwarded to SIEM: %s", event.event_id)
            return {"status": "success", "event_id": event.event_id}

        except Exception as e:
            logger.error("SIEM error: %s", e)
            return {"status": "error", "message": str(e)}

    def _forward_to_syslog(self, event_data: dict):
        try:
            pri = 14
            msg = f"<{pri}>{datetime.now().isoformat()} CentinelaBot {json.dumps(event_data)}"
            self.syslog_socket.sendto(
                msg.encode("utf-8"),
                (Config.SYSLOG_HOST, Config.SYSLOG_PORT)
            )
        except Exception as e:
            logger.error("Syslog forward error: %s", e)

    def query_events(self, filters: dict | None = None) -> list:
        query = SecurityEvent.query
        if filters:
            if "event_type" in filters:
                query = query.filter_by(event_type=filters["event_type"])
            if "severity" in filters:
                query = query.filter_by(severity=filters["severity"])
            if "source" in filters:
                query = query.filter_by(source=filters["source"])
        return [e.to_dict() for e in query.order_by(SecurityEvent.created_at.desc()).limit(100).all()]

    def get_stats(self) -> dict:
        total = SecurityEvent.query.count()
        by_type = dict(
            db.session.query(SecurityEvent.event_type, db.func.count())
            .group_by(SecurityEvent.event_type).all()
        )
        return {"total_events": total, "by_type": by_type}

    def is_healthy(self):
        return True

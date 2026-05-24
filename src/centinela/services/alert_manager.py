import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
from config import Config
from src.centinela.extensions import db
from src.centinela.models.alert import Alert

logger = logging.getLogger("centinela.alert")


class AlertManager:
    def __init__(self):
        self.alert_counter = Alert.query.count()

    def create_alert(self, analysis: dict, source: str = "unknown"):
        self.alert_counter += 1
        severity = analysis.get("severity", "medium")
        alert_id = f"ALT-{1000 + self.alert_counter:04d}"

        alert = Alert(
            alert_id=alert_id,
            title=f"Amenaza {severity.upper()} detectada",
            description=analysis.get("analysis", analysis.get("description", "Sin descripcion")),
            severity=severity,
            source=source,
            status="active",
            event_type=analysis.get("event_type", analysis.get("type", "unknown"))
        )
        db.session.add(alert)
        db.session.commit()
        logger.warning("Alerta creada: %s [%s]", alert_id, severity)

        if severity in ("high", "critical"):
            self._notify_channels(alert)

        return alert.to_dict()

    def _notify_channels(self, alert: Alert):
        if Config.check_smtp():
            self._send_email(alert)
        if Config.check_telegram():
            self._send_telegram(alert)

    def _send_email(self, alert: Alert):
        try:
            msg = MIMEText(
                f"Alerta: {alert.title}\n\n"
                f"ID: {alert.alert_id}\n"
                f"Severidad: {alert.severity}\n"
                f"{alert.description}\n\n-- CentinelaBot"
            )
            msg["Subject"] = f"[CentinelaBot] {alert.title}"
            msg["From"] = Config.SMTP_USER
            msg["To"] = Config.ALERT_EMAIL

            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as s:
                s.starttls()
                s.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
                s.send_message(msg)
            logger.info("Email alert sent: %s", alert.alert_id)
        except Exception as e:
            logger.error("Email failed: %s", e)

    def _send_telegram(self, alert: Alert):
        try:
            import requests
            text = (
                f"\u26a0\ufe0f *Alerta CentinelaBot*\n"
                f"ID: {alert.alert_id}\n"
                f"Severidad: {alert.severity}\n"
                f"{alert.description[:200]}"
            )
            url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, json={
                "chat_id": Config.TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            }, timeout=10)
            logger.info("Telegram alert sent: %s", alert.alert_id)
        except Exception as e:
            logger.error("Telegram failed: %s", e)

    def get_active_alerts(self):
        alerts = Alert.query.filter_by(status="active").order_by(
            Alert.created_at.desc()
        ).all()
        return {
            "total": len(alerts),
            "alerts": [a.to_dict() for a in alerts]
        }

    def resolve_alert(self, alert_id: str):
        alert = Alert.query.filter_by(alert_id=alert_id).first()
        if not alert:
            return None
        alert.status = "resolved"
        alert.resolved_at = datetime.now(timezone.utc)
        db.session.commit()
        return alert.to_dict()

    def is_healthy(self):
        return True

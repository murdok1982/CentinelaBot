import logging
import re
from datetime import datetime, timezone
from src.centinela.extensions import db
from src.centinela.models.event import SecurityEvent

logger = logging.getLogger("centinela.threat")

SUSPICIOUS_PATTERNS = {
    "port_scan": [
        r"scan.*port", r"nmap", r"masscan", r"syn scan", r"port sweep"
    ],
    "brute_force": [
        r"failed.*login", r"brute.?force", r"auth.*fail", r"invalid.*password",
        r"multiple.*auth", r"login.*attempt"
    ],
    "malware": [
        r"malware", r"trojan", r"ransomware", r"backdoor", r"dropper", r"shellcode"
    ],
    "intrusion": [
        r"intrusion", r"unauthorized", r"breach", r"exploit", r"cve-", r"rce"
    ],
    "phishing": [
        r"phish", r"spoof", r"fake.*login", r"suspicious.*url", r"credential.*harvest"
    ],
    "ddos": [
        r"ddos", r"flood", r"amplification", r"syn.*flood", r"traffic.*spike"
    ],
    "data_exfil": [
        r"exfil", r"data.*leak", r"unusual.*outbound", r"dns.*tunnel"
    ],
    "recon": [
        r"recon", r"whois", r"dns.*enum", r"subdomain.*enum", r"dir.*bust"
    ],
}


class ThreatDetector:
    def __init__(self):
        self.event_counter = 0

    def analyze_raw(self, raw_text: str, source: str = "unknown") -> dict | None:
        text_lower = raw_text.lower()
        for threat_type, patterns in SUSPICIOUS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return {
                        "event_type": threat_type,
                        "source": source,
                        "description": f"Patron sospechoso detectado: {pattern}",
                        "severity": self._severity_for(threat_type),
                        "raw_data": raw_text[:500],
                        "status": "open"
                    }
        return None

    def ingest_log_line(self, line: str, source: str = "syslog") -> dict | None:
        threat = self.analyze_raw(line, source)
        if threat:
            event = self._save_event(threat)
            return event.to_dict() if event else threat
        return None

    def _save_event(self, threat_data: dict):
        self.event_counter += 1
        event = SecurityEvent(
            event_id=f"EVT-{1000 + self.event_counter:04d}",
            event_type=threat_data["event_type"],
            severity=threat_data["severity"],
            source=threat_data["source"],
            description=threat_data["description"],
            raw_data=threat_data.get("raw_data", ""),
            status=threat_data.get("status", "open")
        )
        db.session.add(event)
        db.session.commit()
        logger.info("Event saved: %s - %s", event.event_id, event.event_type)
        return event

    def _severity_for(self, threat_type: str) -> str:
        return {
            "port_scan": "low",
            "recon": "low",
            "brute_force": "medium",
            "phishing": "high",
            "malware": "high",
            "intrusion": "critical",
            "ddos": "critical",
            "data_exfil": "critical",
        }.get(threat_type, "medium")

    def get_recent_events(self, limit=50):
        events = SecurityEvent.query.order_by(
            SecurityEvent.created_at.desc()
        ).limit(limit).all()
        return {
            "total": SecurityEvent.query.count(),
            "events": [e.to_dict() for e in events]
        }

    def get_stats(self):
        total = SecurityEvent.query.count()
        by_severity = db.session.query(
            SecurityEvent.severity, db.func.count()
        ).group_by(SecurityEvent.severity).all()
        by_type = db.session.query(
            SecurityEvent.event_type, db.func.count()
        ).group_by(SecurityEvent.event_type).all()
        return {
            "total": total,
            "by_severity": dict(by_severity),
            "by_type": dict(by_type),
        }

    def is_healthy(self):
        return True

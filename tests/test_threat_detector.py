import pytest


def test_threat_detector_analyze():
    from src.centinela.services.threat_detector import ThreatDetector
    td = ThreatDetector()

    result = td.analyze_raw("normal system log entry")
    assert result is None

    result = td.analyze_raw("malware detected on endpoint")
    assert result is not None
    assert result["event_type"] == "malware"

    result = td.analyze_raw("Failed login attempt from 192.168.1.100")
    assert result is not None
    assert result["event_type"] == "brute_force"


def test_threat_detector_ingest():
    from src.centinela.services.threat_detector import ThreatDetector
    td = ThreatDetector()

    result = td.analyze_raw("CVE-2024-1234 exploit attempt")
    assert result is not None
    assert result["event_type"] == "intrusion"

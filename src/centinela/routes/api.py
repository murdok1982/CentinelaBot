from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone

api_bp = Blueprint("api", __name__)

_services = None


def _get_services():
    global _services
    if _services is None:
        from src.centinela.services import AIAnalyzer, ThreatDetector, AlertManager, SIEMIntegration, DashboardService
        _services = {
            "ai": AIAnalyzer(),
            "threat": ThreatDetector(),
            "alerts": AlertManager(),
            "siem": SIEMIntegration(),
            "dash": DashboardService(),
        }
    return _services


@api_bp.route("/")
def index():
    return jsonify({
        "app": "CentinelaBot",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "GET /": "Info del sistema",
            "GET /api/dashboard": "Dashboard data",
            "GET /api/threats": "Amenazas detectadas",
            "POST /api/analyze": "Analizar evento con IA",
            "GET /api/alerts": "Alertas activas",
            "POST /api/alerts/<id>/resolve": "Resolver alerta",
            "GET /api/events": "Eventos de seguridad",
            "POST /api/ingest": "Ingerir log",
            "GET /api/stats": "Estadisticas",
            "GET /api/health": "Health check",
        }
    })


@api_bp.route("/api/dashboard")
@jwt_required(optional=True)
def get_dashboard():
    svc = _get_services()
    return jsonify(svc["dash"].get_summary())


@api_bp.route("/api/threats")
@jwt_required(optional=True)
def get_threats():
    svc = _get_services()
    return jsonify(svc["threat"].get_recent_events())


@api_bp.route("/api/analyze", methods=["POST"])
@jwt_required(optional=True)
def analyze_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    svc = _get_services()
    analysis = svc["ai"].analyze_security_event(data)

    if analysis.get("severity") in ("high", "critical"):
        alert = svc["alerts"].create_alert(analysis, source=data.get("source", "api"))
        analysis["alert"] = alert

    return jsonify(analysis)


@api_bp.route("/api/alerts")
@jwt_required(optional=True)
def get_alerts():
    svc = _get_services()
    return jsonify(svc["alerts"].get_active_alerts())


@api_bp.route("/api/alerts/<alert_id>/resolve", methods=["POST"])
@jwt_required(optional=True)
def resolve_alert(alert_id):
    svc = _get_services()
    result = svc["alerts"].resolve_alert(alert_id)
    if not result:
        return jsonify({"error": "Alerta no encontrada"}), 404
    return jsonify(result)


@api_bp.route("/api/events")
@jwt_required(optional=True)
def get_events():
    svc = _get_services()
    event_type = request.args.get("type")
    severity = request.args.get("severity")
    filters = {}
    if event_type:
        filters["event_type"] = event_type
    if severity:
        filters["severity"] = severity
    return jsonify({"events": svc["siem"].query_events(filters)})


@api_bp.route("/api/ingest", methods=["POST"])
@jwt_required(optional=True)
def ingest_log():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    svc = _get_services()
    raw = data.get("raw", data.get("message", str(data)))
    source = data.get("source", "api")

    threat_data = svc["threat"].ingest_log_line(raw, source)
    if threat_data:
        analysis = svc["ai"].analyze_security_event(threat_data)
        if analysis.get("severity") in ("high", "critical"):
            svc["alerts"].create_alert(analysis, source)
        result = {**threat_data, "analysis": analysis}
    else:
        result = {"status": "clean", "message": "No se detectaron amenazas"}

    svc["siem"].send_event(data)
    return jsonify(result)


@api_bp.route("/api/stats")
@jwt_required(optional=True)
def get_stats():
    svc = _get_services()
    return jsonify({
        "threats": svc["threat"].get_stats(),
        "siem": svc["siem"].get_stats(),
        "dashboard": svc["dash"].get_summary()
    })


@api_bp.route("/api/health")
def health():
    svc = _get_services()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modules": {
            "ai_analyzer": svc["ai"].is_healthy(),
            "threat_detector": svc["threat"].is_healthy(),
            "alert_manager": svc["alerts"].is_healthy(),
            "siem": svc["siem"].is_healthy(),
            "dashboard": svc["dash"].is_healthy(),
        }
    })

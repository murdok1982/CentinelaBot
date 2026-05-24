def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CentinelaBot" in resp.get_json()["app"]


def test_dashboard(client):
    resp = client.get("/api/dashboard")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "statistics" in data


def test_alerts(client):
    resp = client.get("/api/alerts")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "alerts" in data


def test_analyze_no_data(client):
    resp = client.post("/api/analyze", json={})
    assert resp.status_code == 400


def test_analyze_event(client):
    resp = client.post("/api/analyze", json={
        "event_type": "malware",
        "source": "test",
        "description": "Test de malware"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "severity" in data


def test_ingest_clean(client):
    resp = client.post("/api/ingest", json={
        "raw": "normal log entry",
        "source": "test"
    })
    assert resp.status_code == 200


def test_ingest_threat(client):
    resp = client.post("/api/ingest", json={
        "raw": "malware detected in endpoint",
        "source": "test"
    })
    assert resp.status_code == 200


def test_threats_endpoint(client):
    resp = client.get("/api/threats")
    assert resp.status_code == 200


def test_stats(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 200


def test_login_success(client):
    resp = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_login_fail(client):
    resp = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert resp.status_code == 401


def test_register(client):
    resp = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "test123"
    })
    assert resp.status_code == 201


def test_events_endpoint(client):
    resp = client.get("/api/events")
    assert resp.status_code == 200


def test_dashboard_html(client):
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert b"CentinelaBot" in resp.data


def test_alerts_html(client):
    resp = client.get("/alerts")
    assert resp.status_code == 200


def test_login_html(client):
    resp = client.get("/login")
    assert resp.status_code == 200

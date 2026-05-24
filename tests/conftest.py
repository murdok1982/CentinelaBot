import pytest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))


@pytest.fixture
def app():
    os.environ["FLASK_SECRET_KEY"] = "test"
    os.environ["JWT_SECRET"] = "test-jwt"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["AI_PROVIDER"] = "fallback"

    from app import create_app
    app = create_app()
    with app.app_context():
        from src.centinela.extensions import db
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client):
    resp = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    return resp.get_json().get("token", "")

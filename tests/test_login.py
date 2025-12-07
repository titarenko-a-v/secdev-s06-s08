
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_should_not_allow_sql_injection():
    payload = {"username": "admin'-- ", "password": "x"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 401, "SQLi-бэйпас логина должен быть закрыт"


def test_login_wrong_password_should_fail():
    payload = {"username": "admin", "password": "wrong_password_123"}
    resp = client.post("/login", json=payload)

    assert resp.status_code == 401
    assert resp.json() == {"detail": "Invalid credentials"}

from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_chat():
    r = client.post("/chat", json={"session_id":"test","text":"¿Qué servicios ofrecen?"})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data
    assert "category" in data
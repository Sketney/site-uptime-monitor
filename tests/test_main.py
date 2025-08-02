from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

def setup_module(module):
    """Создание таблиц в тестовой SQLite"""
    Base.metadata.create_all(bind=engine)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Site Uptime Monitor is running"}

def test_check_and_history():
    url = "https://example.com"

    check_response = client.get(f"/check?url={url}")
    assert check_response.status_code == 200
    check_data = check_response.json()
    assert check_data["url"] == url
    assert "status_code" in check_data or "error" in check_data

    history_response = client.get("/history")
    assert history_response.status_code == 200
    history_data = history_response.json()

    assert isinstance(history_data, list)
    if "status_code" in check_data:
        assert any(entry["url"] == url for entry in history_data)

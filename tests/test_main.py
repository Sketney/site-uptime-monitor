from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Site Uptime Monitor is running"}

def test_check_and_history():
    url = "https://example.com"

    # Делаем проверку сайта
    check_response = client.get(f"/check?url={url}")
    assert check_response.status_code == 200
    check_data = check_response.json()
    assert check_data["url"] == url
    assert "status_code" in check_data

    # Проверяем, что запись появилась в истории
    history_response = client.get("/history")
    assert history_response.status_code == 200
    history_data = history_response.json()

    assert isinstance(history_data, list)
    assert any(entry["url"] == url for entry in history_data)

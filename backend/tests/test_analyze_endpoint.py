from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_endpoint_productive():
    response = client.post("/analyze", json={"content": "Preciso de suporte"})
    assert response.status_code == 200
    assert response.json()["category"] == "Produtivo"

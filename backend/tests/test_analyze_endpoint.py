from fastapi.testclient import TestClient
from io import BytesIO
import os

from main import app

client = TestClient(app)

os.environ["USE_MOCK_AI"] = "true"


def test_endpoint_productive():
    file = BytesIO(b"Preciso de suporte tecnico urgente")

    response = client.post(
        "/analyze",
        files={"file": ("email.txt", file, "text/plain")}
    )

    assert response.status_code == 200
    body = response.json()
    assert "category" in body
    assert "response" in body
    assert body["filename"] == "email.txt"


def test_endpoint_unproductive():
    file = BytesIO(b"Feliz Natal a todos")

    response = client.post(
        "/analyze",
        files={"file": ("email.txt", file, "text/plain")}
    )

    assert response.status_code == 200


def test_endpoint_empty_content():
    file = BytesIO(b"")

    response = client.post(
        "/analyze",
        files={"file": ("email.txt", file, "text/plain")}
    )

    assert response.status_code == 200

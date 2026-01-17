import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_endpoint_productive():
    response = client.post(
        "/analyze", 
        json={"content": "Preciso de suporte técnico urgente com meu chamado #1234"}
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert data["category"] == "Produtivo"
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0

def test_endpoint_unproductive():
    response = client.post(
        "/analyze", 
        json={"content": "Feliz Natal a todos! Que 2025 seja um ano excelente!"}
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert data["category"] == "Improdutivo"
    assert "response" in data
    assert isinstance(data["response"], str)

def test_endpoint_empty_content():
    response = client.post(
        "/analyze", 
        json={"content": ""}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert data["category"] == "Improdutivo"
    assert "response" in data

def test_endpoint_invalid_json():
    response = client.post("/analyze", json={})
    
    print(f"Invalid JSON response: {response.status_code}, {response.json()}")
    assert response.status_code == 422

def test_endpoint_with_chamado_keyword():
    response = client.post(
        "/analyze", 
        json={"content": "Qual o status do meu chamado?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Produtivo"
    assert "chamado" in data["response"].lower() or "tratado" in data["response"].lower()

def test_endpoint_with_status_keyword():
    response = client.post(
        "/analyze", 
        json={"content": "Gostaria de saber o status da minha solicitação"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Produtivo"

def test_endpoint_with_erro_keyword():
    response = client.post(
        "/analyze", 
        json={"content": "Estou recebendo um erro ao tentar fazer login"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Produtivo"

def test_endpoint_with_suporte_keyword():
    response = client.post(
        "/analyze", 
        json={"content": "Preciso de suporte com a configuração do sistema"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Produtivo"

def test_endpoint_neutral_email():
    response = client.post(
        "/analyze", 
        json={"content": "Bom dia! Espero que todos estejam bem."}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Improdutivo"
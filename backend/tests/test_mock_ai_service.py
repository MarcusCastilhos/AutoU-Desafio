import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.mock_ai_service import MockAIService

def test_email_productive_with_chamado():
    service = MockAIService()
    result = service.analyze_email("Qual o status do meu chamado?")
    
    print(f"Result with 'chamado': {result}")
    assert result["category"] == "Produtivo"
    assert "response" in result
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0
    assert "equipe responsável" in result["response"].lower() or "tratado" in result["response"].lower()

def test_email_productive_with_status():
    service = MockAIService()
    result = service.analyze_email("Status do meu ticket?")
    
    print(f"Result with 'status': {result}")
    assert result["category"] == "Produtivo"

def test_email_productive_with_suporte():
    service = MockAIService()
    result = service.analyze_email("Preciso de suporte técnico")
    
    print(f"Result with 'suporte': {result}")
    assert result["category"] == "Produtivo"

def test_email_productive_with_erro():
    service = MockAIService()
    result = service.analyze_email("O sistema está com erro")
    
    print(f"Result with 'erro': {result}")
    assert result["category"] == "Produtivo"

def test_email_unproductive():
    service = MockAIService()
    result = service.analyze_email("Feliz Natal!")
    
    print(f"Improdutivo result: {result}")
    assert result["category"] == "Improdutivo"
    assert "response" in result
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0
    assert "agradecemos" in result["response"].lower() or "mensagem" in result["response"].lower()

def test_email_mixed_content():
    service = MockAIService()
    
    result1 = service.analyze_email("Preciso de suporte com minha conta")
    assert result1["category"] == "Produtivo"
    
    result2 = service.analyze_email("Obrigado pelo aviso")
    assert result2["category"] == "Improdutivo"
    
    result3 = service.analyze_email("Olá, tudo bem? Meu chamado está parado")
    assert result3["category"] == "Produtivo"

def test_email_edge_cases():
    service = MockAIService()
    
    result1 = service.analyze_email("")
    assert "category" in result1
    assert "response" in result1
    assert result1["category"] == "Improdutivo"
    
    result2 = service.analyze_email("   ")
    assert result2["category"] == "Improdutivo"
    
    long_email = "Bom dia " * 50
    result3 = service.analyze_email(long_email)
    assert result3["category"] == "Improdutivo"

def test_service_implements_interface():
    from services.ai_interface import AIServiceInterface
    
    service = MockAIService()
    
    assert isinstance(service, AIServiceInterface)
    
    assert hasattr(service, 'analyze_email')
    assert callable(getattr(service, 'analyze_email'))
    
    result = service.analyze_email("teste")
    assert isinstance(result, dict)
    assert "category" in result
    assert "response" in result
    assert result["category"] in ["Produtivo", "Improdutivo"]

def test_case_insensitive():
    service = MockAIService()
    
    result1 = service.analyze_email("PRECISO DE SUPORTE")
    assert result1["category"] == "Produtivo"
    
    result2 = service.analyze_email("ChAmAdO #1234")
    assert result2["category"] == "Produtivo"
    
    result3 = service.analyze_email("erro no sistema")
    assert result3["category"] == "Produtivo"
from services.mock_ai_service import MockAIService

def test_email_productive():
    service = MockAIService()
    result = service.analyze_email("Qual o status do meu chamado?")
    assert result["category"] == "Produtivo"

def test_email_unproductive():
    service = MockAIService()
    result = service.analyze_email("Feliz Natal!")
    assert result["category"] == "Improdutivo"

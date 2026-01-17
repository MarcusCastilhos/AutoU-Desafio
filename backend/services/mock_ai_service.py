from services.ai_interface import AIServiceInterface

class MockAIService(AIServiceInterface):

    def analyze_email(self, email_text: str) -> dict:
        text = email_text.lower()

        if any(word in text for word in ["chamado", "status", "suporte", "erro"]):
            return {
                "category": "Produtivo",
                "response": "Seu email foi recebido e será tratado pela equipe responsável."
            }

        return {
            "category": "Improdutivo",
            "response": "Agradecemos a mensagem! Retornaremos assim que possível."
        }

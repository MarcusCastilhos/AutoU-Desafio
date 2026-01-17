import os
import json
from openai import OpenAI
from services.ai_interface import AIServiceInterface


class OpenAIService(AIServiceInterface):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não configurada. "
                "Defina a variável de ambiente ou use USE_MOCK_AI=true."
            )

        self.client = OpenAI(api_key=api_key)

    def analyze_email(self, email_text: str) -> dict:
        prompt = f"""
Você é um sistema que classifica emails corporativos.

Classifique o email abaixo em:
- Produtivo
- Improdutivo

Depois gere uma resposta automática adequada.

Retorne SOMENTE um JSON válido no formato:
{{
  "category": "Produtivo ou Improdutivo",
  "response": "Texto da resposta automática"
}}

Email:
\"\"\"
{email_text}
\"\"\"
"""

        try:
            response = self.client.responses.create(
                model="gpt-4o-mini",
                input=prompt,
                temperature=0.2,
            )

            raw_content = response.output_text
            return json.loads(raw_content)

        except Exception as e:
            return {
                "category": "Erro",
                "response": f"Erro ao processar com OpenAI: {str(e)}",
            }

import os
from openai import OpenAI
from services.ai_interface import AIServiceInterface

class OpenAIExecutor(AIServiceInterface):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não configurada")
        self.client = OpenAI(api_key=api_key)

    def execute(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=0.2,
        )
        return response.output_text

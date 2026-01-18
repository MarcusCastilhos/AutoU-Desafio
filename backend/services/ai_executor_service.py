from services.ai_interface import AIServiceInterface

class AIExecutorService:
    def __init__(self, provider: AIServiceInterface):
        self.provider = provider

    def run(self, prompt: str) -> str:
        return self.provider.execute(prompt)

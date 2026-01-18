from services.ai_interface import AIServiceInterface
from services.mock_ai_service import MockAIService
import json


class MockExecutor(AIServiceInterface):
    def __init__(self):
        self.mock = MockAIService()

    def execute(self, prompt: str) -> str:
        email_text = prompt.split('"""')[1]
        result = self.mock.analyze_email(email_text)
        return json.dumps(result)

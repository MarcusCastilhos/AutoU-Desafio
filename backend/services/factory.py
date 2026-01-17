import os
from services.ai_interface import AIServiceInterface
from services.openai_service import OpenAIService
from services.mock_ai_service import MockAIService

def get_ai_service() -> AIServiceInterface:
    use_mock = os.getenv("USE_MOCK_AI", "true").lower() == "true"

    if use_mock:
        return MockAIService()

    return OpenAIService()

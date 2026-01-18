import os
from services.ai_executor_service import AIExecutorService
from services.openai_executor import OpenAIExecutor
from services.mock_executor import MockExecutor

def get_ai_executor() -> AIExecutorService:
    use_mock = os.getenv("USE_MOCK_AI", "true").lower() == "true"

    provider = MockExecutor() if use_mock else OpenAIExecutor()
    return AIExecutorService(provider)

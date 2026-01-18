import json
from services.factory import get_ai_executor
from prompts.email_analysis_prompt import build_email_analysis_prompt

class AnalyzeEmailUseCase:

    async def execute(self, email_text: str) -> dict:
        prompt = build_email_analysis_prompt(email_text)

        executor = get_ai_executor()
        raw_result = executor.run(prompt)

        return json.loads(raw_result)

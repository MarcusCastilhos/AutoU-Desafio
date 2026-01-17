import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

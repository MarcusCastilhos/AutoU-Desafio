from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.email_schema import EmailRequest, EmailResponse
from services.factory import get_ai_service

app = FastAPI(title="Email Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=EmailResponse)
async def analyze_email(request: EmailRequest):
    ai_service = get_ai_service()
    result = ai_service.analyze_email(request.content)
    return result
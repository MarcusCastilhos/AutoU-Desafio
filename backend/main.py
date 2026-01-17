from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.email_schema import EmailRequest
from services.factory import get_ai_service
from routes.analyze import router as analyze_router

app = FastAPI(title="Email Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)

@app.post("/analyze")
def analyze_email(request: EmailRequest):
    ai_service = get_ai_service()
    result = ai_service.analyze_email(request.content)
    return result

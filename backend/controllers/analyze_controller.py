from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.file_reader import extract_text_from_file
from usecases.analyze_email_usecase import AnalyzeEmailUseCase

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("")
async def analyze_email(file: UploadFile = File(...)):
    try:
        text = await extract_text_from_file(file)

        usecase = AnalyzeEmailUseCase()
        result = await usecase.execute(text)

        return {
            "filename": file.filename,
            "category": result["category"],
            "response": result["response"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

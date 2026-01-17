from fastapi import APIRouter, UploadFile, File, HTTPException
from services.factory import get_ai_service
from services.file_reader import extract_text_from_file

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("")
async def analyze_email(file: UploadFile = File(...)):
    try:
        text = await extract_text_from_file(file)

        ai_service = get_ai_service()
        result = ai_service.analyze_email(text)

        return {
            "filename": file.filename,
            "category": result["category"],
            "response": result["response"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

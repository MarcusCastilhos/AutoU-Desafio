from pydantic import BaseModel

class EmailRequest(BaseModel):
    content: str

class EmailResponse(BaseModel):
    category: str
    response: str
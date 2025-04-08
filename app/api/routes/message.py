
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional 

from app.schemas.message import MessageRequest, MessageResponse
from app.services.ai_service import AIService

router = APIRouter()

# Dependency to get the AI service
def get_ai_service():
    return AIService()


# Request model
class MessageRequest(BaseModel):
    message: str
    user_id: int
@router.post("/analyze", response_model=MessageResponse)
async def analyze_message(
    request: MessageRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Analyze a message using OpenAI and extract structured expense data.
    
    - **message**: The message to be analyzed
    
    Returns structured data: amount, category, description.
    """
    if not request.message or request.message.strip() == "":
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Get structured response
    response = await ai_service.process_message(request.message, request.user_id)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    return MessageResponse(**response)

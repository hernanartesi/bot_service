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
    
    try:
        # Get structured response
        response = await ai_service.process_message(request.message, request.user_id)
        
        # Check if response is None
        if response is None:
            return MessageResponse(
                type="error",
                data=None,
                error="An unexpected error occurred while processing your message"
            )
            
        # The response is already a MessageResponse object, so return it directly
        return response
    except Exception as e:
        # Log the exception
        print(f"Error in analyze_message: {str(e)}")
        # Return a fallback MessageResponse
        return MessageResponse(
            type="error",
            data=None,
            error=f"An error occurred: {str(e)}"
        )

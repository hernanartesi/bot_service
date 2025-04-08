from pydantic import BaseModel, Field

class MessageRequest(BaseModel):
    """Model for incoming message requests."""
    message: str = Field(..., description="The message to analyze")
    
class MessageResponse(BaseModel):
    """Model for API responses."""
    amount: float
    category: str
    description: str
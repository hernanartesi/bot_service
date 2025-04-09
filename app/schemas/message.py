from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any
from datetime import datetime

class MessageRequest(BaseModel):
    """Model for incoming message requests."""
    message: str = Field(..., description="The message to analyze")
    user_id: int
    
class ExpenseData(BaseModel):
    """Model for expense data."""
    amount: float
    category: str
    description: str

class SummaryData(BaseModel):
    """Model for summary data."""
    id: int
    description: str
    amount: float
    category: str
    added_at: datetime

class ErrorResponse(BaseModel):
    """Model for error data."""
    message: str = "An error occurred"

class MessageResponse(BaseModel):
    """Model for API responses."""
    type: str
    data: Optional[Union[ExpenseData, List[SummaryData], dict, None]] = None
    error: Optional[str] = None
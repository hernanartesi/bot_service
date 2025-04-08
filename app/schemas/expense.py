from datetime import datetime
from pydantic import BaseModel, Field

class ExpenseBase(BaseModel):
    description: str
    amount: float = Field(ge=0)
    category: str

class ExpenseCreate(ExpenseBase):
    user_id: int

class Expense(ExpenseBase):
    id: int
    user_id: int
    added_at: datetime

    class Config:
        from_attributes = True 
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field

class ExpenseFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[str] = None
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)
    
    def to_sql_where_clause(self) -> str:
        """Convert filter to SQL WHERE clause."""
        conditions = []
        if self.start_date:
            conditions.append(f"added_at >= '{self.start_date.isoformat()}'")
        if self.end_date:
            conditions.append(f"added_at <= '{self.end_date.isoformat()}'")
        if self.category:
            conditions.append(f"category = '{self.category}'")
        if self.min_amount is not None:
            conditions.append(f"amount >= {self.min_amount}")
        if self.max_amount is not None:
            conditions.append(f"amount <= {self.max_amount}")
        
        return " AND ".join(conditions) if conditions else "1=1" 
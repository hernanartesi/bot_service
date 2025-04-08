from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(MONEY, nullable=False)
    category = Column(String, nullable=False)
    added_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow) 
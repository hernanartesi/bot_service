from typing import Optional, List
from app.core.database import SessionLocal
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate
from app.schemas.expense_filter import ExpenseFilter
from datetime import datetime
from sqlalchemy import text, Numeric
from decimal import Decimal

class ExpenseService:
    @staticmethod
    def create_expense(expense: ExpenseCreate) -> Optional[Expense]:
        """
        Create a new expense in the database.
        
        Args:
            expense: The expense data to create
            
        Returns:
            The created expense or None if creation failed
        """
        db = SessionLocal()
        print(expense)
        try:
            db_expense = Expense(
                user_id=expense.user_id,
                description=expense.description,
                amount=Decimal(str(expense.amount)),  # Convert to Decimal for exact precision
                category=expense.category,
                added_at=datetime.utcnow()  # Explicitly set the timestamp
            )
            db.add(db_expense)
            db.commit()
            db.refresh(db_expense)
            return db_expense
        except Exception as e:
            db.rollback()
            print(e)
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_expenses_by_user(user_id: int, filters: Optional[ExpenseFilter] = None) -> List[Expense]:
        """
        Get all expenses for a specific user with optional filters.
        
        Args:
            user_id: The ID of the user
            filters: Optional filters to apply to the query
            
        Returns:
            List of expenses for the user matching the filters
        """
        db = SessionLocal()
        try:
            query = db.query(Expense).filter(Expense.user_id == user_id)
            
            if filters:
                if filters.start_date:
                    query = query.filter(Expense.added_at >= filters.start_date)
                if filters.end_date:
                    query = query.filter(Expense.added_at <= filters.end_date)
                if filters.category:
                    query = query.filter(Expense.category == filters.category)
                if filters.min_amount is not None:
                    query = query.filter(Expense.amount >= filters.min_amount)
                if filters.max_amount is not None:
                    query = query.filter(Expense.amount <= filters.max_amount)
            
            return query.all()
        finally:
            db.close()
    
    @staticmethod
    def get_expenses_sql(user_id: int, filters: Optional[ExpenseFilter] = None) -> str:
        """
        Generate SQL query for expenses with filters.
        
        Args:
            user_id: The ID of the user
            filters: Optional filters to apply
            
        Returns:
            SQL query string
        """
        base_query = f"SELECT * FROM expenses WHERE user_id = {user_id}"
        if filters:
            where_clause = filters.to_sql_where_clause()
            if where_clause != "1=1":
                base_query += f" AND {where_clause}"
        return base_query 
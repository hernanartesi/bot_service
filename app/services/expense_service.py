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
        try:
            # Use raw SQL to properly handle money type
            sql = text("""
                INSERT INTO expenses (user_id, description, amount, category, added_at)
                VALUES (:user_id, :description, CAST(:amount AS money), :category, :added_at)
                RETURNING *
            """)
            result = db.execute(
                sql,
                {
                    'user_id': expense.user_id,
                    'description': expense.description,
                    'amount': str(expense.amount),  # Convert float to string for casting
                    'category': expense.category,
                    'added_at': datetime.utcnow()
                }
            )
            db.commit()
            # Convert the result to an Expense model instance
            row = result.fetchone()
            if row:
                return Expense(
                    id=row.id,
                    user_id=row.user_id,
                    description=row.description,
                    amount=row.amount,
                    category=row.category,
                    added_at=row.added_at
                )
            return None
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
from typing import Optional, List
from contextlib import contextmanager
from app.core.database import SessionLocal
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate
from app.schemas.expense_filter import ExpenseFilter
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class ExpenseService:
    @staticmethod
    @contextmanager
    def get_db_session():
        """Provide a transactional scope around a series of operations."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def _parse_money_amount(amount_str: str) -> float:
        """Convert a money string to float by removing currency symbol and parsing."""
        if isinstance(amount_str, (int, float)):
            return float(amount_str)
        return float(amount_str.replace('$', '').replace(',', ''))

    @staticmethod
    def create_expense(expense: ExpenseCreate) -> Optional[Expense]:
        """
        Create a new expense in the database.
        
        Args:
            expense: The expense data to create
            
        Returns:
            The created expense or None if creation failed
        """
        with ExpenseService.get_db_session() as db:
            try:
                # Set isolation level for money transactions
                db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                
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
                
                # Convert the result to an Expense model instance
                row = result.fetchone()
                if row:
                    # Parse the money amount back to float
                    amount = ExpenseService._parse_money_amount(row.amount)
                    expense_obj = Expense(
                        id=row.id,
                        user_id=row.user_id,
                        description=row.description,
                        amount=amount,  # Use the parsed float value
                        category=row.category,
                        added_at=row.added_at
                    )
                    db.commit()
                    return expense_obj
                return None
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Database error: {str(e)}")
                return None
            except Exception as e:
                db.rollback()
                print(f"Unexpected error: {str(e)}")
                return None

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
        with ExpenseService.get_db_session() as db:
            try:
                # Set READ COMMITTED for consistent reads
                db.execute(text("SET TRANSACTION ISOLATION LEVEL READ COMMITTED"))
                
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
            except SQLAlchemyError as e:
                print(f"Database error: {str(e)}")
                return []
    
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
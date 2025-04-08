from app.core.database import SessionLocal
from app.models.expense_category import ExpenseCategory

class ExpenseCategoryService:
    @staticmethod
    def get_all_categories() -> list[ExpenseCategory]:
        """Get all expense categories from the database."""
        db = SessionLocal()
        try:
            return db.query(ExpenseCategory).all()
        finally:
            db.close()
    
    @staticmethod
    def get_categories_as_string() -> str:
        """Get all expense categories as a comma-separated string."""
        categories = ExpenseCategoryService.get_all_categories()
        return ", ".join([cat.name for cat in categories]) 
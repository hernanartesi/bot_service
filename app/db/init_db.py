from app.core.database import SessionLocal, engine, Base
from app.models.expense_category import ExpenseCategory

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize categories
    default_categories = [
        "Housing",
        "Transportation",
        "Food",
        "Utilities",
        "Insurance",
        "Medical/Healthcare",
        "Savings",
        "Debt",
        "Education",
        "Entertainment",
        "Other"
    ]
    
    db = SessionLocal()
    try:
        # Check if categories already exist
        existing_categories = db.query(ExpenseCategory).all()
        if not existing_categories:
            # Add default categories
            for category_name in default_categories:
                category = ExpenseCategory(name=category_name)
                db.add(category)
            db.commit()
            print("Default categories added successfully")
        else:
            print("Categories already exist in the database")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 
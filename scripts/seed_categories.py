import os
import psycopg
from dotenv import load_dotenv

def seed_categories():
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Default categories
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
    
    # Connect to the database
    conn = psycopg.connect(DATABASE_URL)
    
    try:
        # Create a cursor
        cur = conn.cursor()
        
        # Insert default categories
        for category in default_categories:
            cur.execute(
                "INSERT INTO expense_categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (category,)
            )
        
        # Commit the transaction
        conn.commit()
        print("Default categories added successfully!")
        
    except Exception as e:
        print(f"Error seeding categories: {e}")
        conn.rollback()
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_categories() 
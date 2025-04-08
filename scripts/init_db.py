import os
import psycopg
from dotenv import load_dotenv

def init_db():
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Connect to the database
    conn = psycopg.connect(DATABASE_URL)
    
    try:
        # Create a cursor
        cur = conn.cursor()
        
        # Read and execute the SQL file
        with open('init_db.sql', 'r') as file:
            sql_commands = file.read()
            cur.execute(sql_commands)
        
        # Commit the transaction
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_db() 
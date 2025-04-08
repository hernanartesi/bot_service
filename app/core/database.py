from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# Define Base here
Base = declarative_base()

# Handle both local development and Railway deployment
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith('postgresql://') and not DATABASE_URL.startswith('postgresql+psycopg://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Check if tables exist before creating them
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

# Only create tables that don't exist
for table in Base.metadata.tables:
    if table not in existing_tables:
        Base.metadata.tables[table].create(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
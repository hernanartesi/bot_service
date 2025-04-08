from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Define Base here
Base = declarative_base()

# Using psycopg3 dialect
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
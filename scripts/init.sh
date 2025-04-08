#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h $PGHOST -p $PGPORT -q -U $PGUSER; do
  sleep 1
done

# Run the initialization scripts
echo "Initializing database..."
python scripts/init_db.py

echo "Seeding categories..."
python scripts/seed_categories.py

echo "Database initialization complete!" 
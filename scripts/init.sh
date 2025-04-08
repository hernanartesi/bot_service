#!/bin/bash

# Run the initialization scripts
echo "Initializing database..."
python scripts/init_db.py

echo "Seeding categories..."
python scripts/seed_categories.py

echo "Database initialization complete!" 
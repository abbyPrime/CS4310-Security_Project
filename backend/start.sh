#!/bin/bash

# Exit on error, but allow database initialization to fail gracefully
echo "=== Railway Deployment Startup ==="
echo "Checking environment variables..."

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set!"
    echo "Please add a PostgreSQL database to your Railway project."
    exit 1
fi

echo "DATABASE_URL is set: ${DATABASE_URL:0:30}..."

# Check if PORT is set
if [ -z "$PORT" ]; then
    echo "WARNING: PORT is not set, using default 8000"
    PORT=8000
fi

echo "PORT is set: $PORT"

# Initialize database (allow failures for idempotency)
echo ""
echo "=== Initializing database tables ==="
python init_db.py || echo "Note: Database initialization skipped (may already exist)"

# Create test users (allow failures for idempotency)
echo ""
echo "=== Creating test users ==="
python create_test_users.py || echo "Note: Test user creation skipped (may already exist)"

# Start the application
echo ""
echo "=== Starting FastAPI application ==="
echo "Listening on 0.0.0.0:$PORT"
exec uvicorn main:app --host 0.0.0.0 --port $PORT

#!/bin/bash
set -e

echo "=== Railway Deployment Startup ==="
echo "Timestamp: $(date)"
echo ""

# Check if DATABASE_URL is set
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set!"
    echo "Please add a PostgreSQL database to your Railway project."
    exit 1
fi
echo "✓ DATABASE_URL is set: ${DATABASE_URL:0:30}..."

# Check if PORT is set
if [ -z "$PORT" ]; then
    echo "WARNING: PORT is not set, using default 8000"
    PORT=8000
fi
echo "✓ PORT is set: $PORT"

# Wait a moment for database to be ready
echo ""
echo "Waiting for database to be ready..."
sleep 2

# Initialize database (continue on error)
echo ""
echo "=== Initializing database tables ==="
if python init_db.py 2>&1; then
    echo "✓ Database initialization completed"
else
    echo "⚠ Database initialization had warnings (this is OK if tables already exist)"
fi

# Create test users (continue on error)
echo ""
echo "=== Creating test users ==="
if python create_test_users.py 2>&1; then
    echo "✓ Test users created"
else
    echo "⚠ Test user creation had warnings (this is OK if users already exist)"
fi

# Start the application
echo ""
echo "=== Starting FastAPI application ==="
echo "Service: CinemaShare API"
echo "Listening on: 0.0.0.0:$PORT"
echo "Health check: http://0.0.0.0:$PORT/health"
echo "API docs: http://0.0.0.0:$PORT/docs"
echo ""
echo "Starting uvicorn..."

exec uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info

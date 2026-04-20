#!/usr/bin/env bash
# Render build script

set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python init_db.py

# Create test users (optional - comment out for production)
python create_test_users.py

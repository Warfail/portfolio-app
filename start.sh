#!/bin/bash
echo "🚀 Starting Portfolio Application..."
echo "====================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Verify uvicorn is installed
echo "🔍 Checking uvicorn..."
python -c "import uvicorn; print('✅ uvicorn installed')"

# Run the app
echo "🚀 Starting server..."
cd backend
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
#!/bin/bash

# Prosparity Collection Dashboard Backend Startup Script

echo "🚀 Starting Prosparity Collection Dashboard Backend..."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected: backend/"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 is not installed or not in PATH"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if database tables exist
echo "🔍 Checking database connection..."
if python3 -c "
import sys
sys.path.append('.')
from app.db.session import SessionLocal
try:
    db = SessionLocal()
    db.execute('SELECT 1')
    db.close()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
"; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed. Please check your database configuration."
    exit 1
fi

# Start the server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation will be available at:"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

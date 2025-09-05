#!/bin/bash

# Prosparity Collection Dashboard Backend Setup Script

echo "🔧 Setting up Prosparity Collection Dashboard Backend..."

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
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing and recreating..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Check database configuration
echo "🔍 Checking database configuration..."
if [ ! -f "app/core/config.py" ]; then
    echo "❌ Database configuration file not found"
    exit 1
fi

echo "✅ Database configuration file found"

# Test database connection
echo "🔍 Testing database connection..."
python3 -c "
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
    print('Please check your database configuration in app/core/config.py')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Database connection failed"
    echo "   Please check your MySQL server is running and database exists"
    echo "   Update DATABASE_URL in app/core/config.py if needed"
    exit 1
fi

echo "✅ Database connection successful"

# Initialize database tables
echo "🗄️  Initializing database tables..."
python3 -m app.db.init_db

if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database tables"
    exit 1
fi

echo "✅ Database tables created"

# Populate initial data
echo "📊 Populating initial data..."
python3 -m app.db.populate_repayment_status

if [ $? -ne 0 ]; then
    echo "❌ Failed to populate initial data"
    exit 1
fi

echo "✅ Initial data populated"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the backend server, run:"
echo "   ./start.sh                    # On macOS/Linux"
echo "   start.bat                     # On Windows"
echo ""
echo "Or manually:"
echo "   source venv/bin/activate"
echo "   python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "The API will be available at:"
echo "   - Server: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""

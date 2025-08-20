@echo off
REM Prosparity Collection Dashboard Backend Startup Script for Windows

echo 🚀 Starting Prosparity Collection Dashboard Backend...

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ❌ Error: Please run this script from the backend directory
    echo    Current directory: %CD%
    echo    Expected: backend\
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Check if database tables exist
echo 🔍 Checking database connection...
python -c "
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
"

if errorlevel 1 (
    echo ❌ Database connection failed. Please check your database configuration.
    pause
    exit /b 1
)

echo ✅ Database connection successful

REM Start the server
echo 🌐 Starting FastAPI server on http://localhost:8000
echo 📚 API Documentation will be available at:
echo    - Swagger UI: http://localhost:8000/docs
echo    - ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause

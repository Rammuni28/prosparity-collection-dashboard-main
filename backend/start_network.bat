@echo off
echo 🚀 Starting Prosparity Backend with Network Access
echo ==================================================

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Find your PC's IP address
echo 🔍 Finding your PC's IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set IP_ADDRESS=%%a
    goto :found_ip
)
:found_ip
set IP_ADDRESS=%IP_ADDRESS: =%

echo ✅ Your PC's IP Address: %IP_ADDRESS%
echo 🌐 Backend will be accessible at: http://%IP_ADDRESS%:8000
echo 📱 Android devices can use: http://%IP_ADDRESS%:8000
echo.

REM Start the server with network access
echo 🚀 Starting FastAPI server on all network interfaces...
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

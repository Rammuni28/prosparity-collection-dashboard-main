#!/bin/bash

echo "🚀 Starting Prosparity Backend with Network Access"
echo "=================================================="

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Find your PC's IP address
echo "🔍 Finding your PC's IP address..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP_ADDRESS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    IP_ADDRESS=$(ip addr show | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d'/' -f1 | head -1)
else
    # Windows (if using Git Bash)
    IP_ADDRESS=$(ipconfig | grep "IPv4" | awk '{print $NF}' | head -1)
fi

echo "✅ Your PC's IP Address: $IP_ADDRESS"
echo "🌐 Backend will be accessible at: http://$IP_ADDRESS:8000"
echo "📱 Android devices can use: http://$IP_ADDRESS:8000"
echo ""

# Start the server with network access
echo "🚀 Starting FastAPI server on all network interfaces..."
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

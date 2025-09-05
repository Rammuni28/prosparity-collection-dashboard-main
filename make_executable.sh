#!/bin/bash

echo "🔧 Making scripts executable..."

# Make backend script executable
chmod +x start_network.sh
echo "✅ Backend script is now executable"

# Make frontend script executable (if it exists)
if [ -f "../Front-end/start_network.sh" ]; then
    chmod +x ../Front-end/start_network.sh
    echo "✅ Frontend script is now executable"
fi

echo "🎉 All scripts are now executable!"
echo ""
echo "To start backend: ./start_network.sh"
echo "To start frontend: cd ../Front-end && ./start_network.sh"

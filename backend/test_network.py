#!/usr/bin/env python3
"""
Network Connectivity Test Script
Tests if your backend is accessible from the network
"""

import socket
import requests
import subprocess
import sys
from pathlib import Path

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def test_port_open(host, port):
    """Test if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def test_backend_health(host, port):
    """Test backend health endpoint"""
    try:
        response = requests.get(f"http://{host}:{port}/docs", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def main():
    print("🌐 Network Connectivity Test")
    print("=" * 40)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📍 Your Local IP: {local_ip}")
    
    # Test backend port
    backend_port = 8000
    print(f"\n🔍 Testing Backend Port {backend_port}...")
    
    if test_port_open("0.0.0.0", backend_port):
        print(f"✅ Backend port {backend_port} is open on all interfaces")
    else:
        print(f"❌ Backend port {backend_port} is not accessible")
        print("   Make sure to start backend with: --host 0.0.0.0")
    
    # Test localhost
    if test_port_open("127.0.0.1", backend_port):
        print(f"✅ Backend accessible on localhost:{backend_port}")
    else:
        print(f"❌ Backend not accessible on localhost:{backend_port}")
    
    # Test local IP
    if test_port_open(local_ip, backend_port):
        print(f"✅ Backend accessible on {local_ip}:{backend_port}")
    else:
        print(f"❌ Backend not accessible on {local_ip}:{backend_port}")
    
    # Test backend health
    print(f"\n🏥 Testing Backend Health...")
    if test_backend_health(local_ip, backend_port):
        print(f"✅ Backend is healthy and responding on {local_ip}:{backend_port}")
    else:
        print(f"❌ Backend is not responding on {local_ip}:{backend_port}")
    
    print(f"\n📱 For Android devices, use:")
    print(f"   Backend: http://{local_ip}:{backend_port}")
    print(f"   Frontend: http://{local_ip}:5173")
    
    print(f"\n🔧 To start backend with network access:")
    print(f"   cd backend && ./start_network.sh")
    print(f"   or on Windows: start_network.bat")

if __name__ == "__main__":
    main()

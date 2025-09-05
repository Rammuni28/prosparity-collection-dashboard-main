# 🌐 Network Setup Guide for Prosparity Collection Dashboard

This guide will help you make your local backend and frontend accessible from Android devices and other network devices.

## 🚀 Quick Start

### **Option 1: Use Scripts (Recommended)**

#### **For Mac/Linux:**
```bash
# Make scripts executable
cd backend
chmod +x make_executable.sh
./make_executable.sh

# Start backend with network access
./start_network.sh

# In another terminal, start frontend
cd ../Front-end
./start_network.sh
```

#### **For Windows:**
```cmd
# Start backend with network access
cd backend
start_network.bat

# In another command prompt, start frontend
cd Front-end
start_network.bat
```

### **Option 2: Manual Commands**

#### **Start Backend:**
```bash
cd backend
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate.bat  # Windows

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### **Start Frontend:**
```bash
cd Front-end
npm run dev -- --host 0.0.0.0
```

## 📱 Access from Android Devices

### **Find Your PC's IP Address:**
- **Mac/Linux:** `ifconfig | grep "inet " | grep -v 127.0.0.1`
- **Windows:** `ipconfig`

### **Access URLs:**
- **Backend API:** `http://YOUR_IP:8000`
- **Frontend:** `http://YOUR_IP:5173`
- **API Documentation:** `http://YOUR_IP:8000/docs`

## 🔧 Configuration Changes Made

### **1. Backend CORS Settings**
- Updated `backend/app/core/config.py` to allow network access
- Added wildcard origins for development

### **2. Frontend API Configuration**
- Updated `Front-end/src/integrations/api/client.ts` to use network IP
- Added fallback options for different network configurations

### **3. Network Scripts**
- `backend/start_network.sh` - Start backend with network access
- `Front-end/start_network.sh` - Start frontend with network access
- `backend/start_network.bat` - Windows version for backend
- `Front-end/start_network.bat` - Windows version for frontend

## 🧪 Testing Network Connectivity

### **Run Network Test:**
```bash
cd backend
python test_network.py
```

This script will:
- Find your local IP address
- Test if ports are open
- Verify backend health
- Provide access URLs for Android devices

## 🚨 Troubleshooting

### **Common Issues:**

#### **1. Connection Refused**
- Make sure backend is running with `--host 0.0.0.0`
- Check if port 8000 is not blocked by firewall

#### **2. CORS Errors**
- Backend CORS is already configured for network access
- Make sure you're using the correct IP address

#### **3. Port Already in Use**
- Kill existing processes: `lsof -ti:8000 | xargs kill -9`
- Or use different port: `--port 8001`

#### **4. Firewall Issues**
- **Mac:** System Preferences → Security & Privacy → Firewall
- **Windows:** Windows Defender Firewall → Allow app through firewall
- **Linux:** `sudo ufw allow 8000`

### **Network Commands:**

#### **Check Listening Ports:**
```bash
# Mac/Linux
lsof -i :8000
netstat -an | grep 8000

# Windows
netstat -an | findstr 8000
```

#### **Test Connectivity:**
```bash
# Test from PC
curl http://localhost:8000/docs
curl http://YOUR_IP:8000/docs

# Test from Android device
# Use browser: http://YOUR_IP:8000/docs
```

## 🔒 Security Notes

### **Development Only:**
- Current CORS settings allow all origins (`*`)
- Server bound to all interfaces (`0.0.0.0`)
- No authentication required for network access

### **Production:**
- Restrict CORS to specific origins
- Use reverse proxy (nginx)
- Implement proper authentication
- Bind to specific network interfaces

## 📋 Checklist

- [ ] Backend running on `--host 0.0.0.0 --port 8000`
- [ ] Frontend running on `--host 0.0.0.0 --port 5173`
- [ ] CORS configured for network access
- [ ] Firewall allows port 8000 and 5173
- [ ] Android device connected to same network
- [ ] Test connectivity with `test_network.py`
- [ ] Access from Android device successful

## 🆘 Need Help?

If you encounter issues:

1. Run `python test_network.py` to diagnose problems
2. Check firewall settings
3. Verify network connectivity
4. Ensure both backend and frontend are running with network access

## 🎯 Success Indicators

- ✅ Backend accessible at `http://YOUR_IP:8000/docs`
- ✅ Frontend accessible at `http://YOUR_IP:5173`
- ✅ Android device can load both URLs
- ✅ No CORS errors in browser console
- ✅ API calls work from frontend

---

**Happy Networking! 🚀📱**

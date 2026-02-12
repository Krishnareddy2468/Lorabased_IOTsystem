# 🚀 SmartAgro - Quick Start Guide

## ⚡ Fastest Way to Get Started

### 1. Run Setup Script

```bash
./setup.sh
```

This will:
- ✓ Check Python and Node.js installations
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Verify Firebase credentials

### 2. Get Firebase Credentials

**Required**: Download your Firebase service account key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `agrivision-1e11f`
3. Click ⚙️ **Project Settings** → **Service Accounts**
4. Click **Generate New Private Key**
5. Save file as `serviceAccountKey.json` in project root

### 3. Start the Application

**Terminal 1 - Flask API:**
```bash
source venv/bin/activate
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd public
python3 -m http.server 8000
```

**Terminal 3 - Push Test Data (Optional):**
```bash
source venv/bin/activate
python3 push_test_data.py continuous /sensor_data 5
```

### 4. Access Dashboard

Open browser: **http://localhost:8000/login.html**

- Create account or login
- Dashboard will show live sensor data

---

## 🧪 Testing the System

### Test 1: API Health Check

```bash
curl http://127.0.0.1:5001/
```

Expected: `{"message": "Flask API is running! Use POST /predict to get predictions."}`

### Test 2: Send Prediction Request

```bash
curl -X POST http://127.0.0.1:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "soil": 250,
    "light": 400,
    "temperature": 35,
    "humidity": 40,
    "pH": 7.0,
    "npk": 25,
    "rainfall": 10
  }'
```

Expected: JSON with `irrigation_needed`, `confidence`, and `reason`

### Test 3: Push Test Data to Firebase

```bash
# Single push
python3 push_test_data.py once

# Continuous (every 5 seconds)
python3 push_test_data.py continuous /sensor_data 5
```

### Test 4: Fetch and Predict

```bash
# Fetch once
python3 fetch_and_predict.py once

# Listen continuously
python3 fetch_and_predict.py listen /sensor_data 5
```

---

## 📊 Data Flow

```
Push Test Data → Firebase → Fetch Script → Flask API → Prediction → Firestore → Dashboard
```

---

## 🐛 Common Issues

### "Module not found" error
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 5001 already in use"
```bash
# Kill process on port 5001
lsof -i :5001
kill -9 <PID>
```

### "Firebase permission denied"
- Check `serviceAccountKey.json` exists
- Verify Firebase Database rules allow read/write
- Check Database URL in scripts

### Dashboard not loading
- Check browser console (F12)
- Verify `dummy_data.json` exists in `public/`
- Try hard refresh (Cmd+Shift+R / Ctrl+Shift+R)

---

## 📁 Project Structure (Simplified)

```
IOT WEBAPP/
├── app.py                    # Flask API (port 5001)
├── requirements.txt          # Python dependencies
├── serviceAccountKey.json    # Firebase credentials (YOU NEED THIS!)
├── irrigation_model.pkl      # ML model
├── push_test_data.py        # Push sensor data to Firebase
├── fetch_and_predict.py     # Fetch from Firebase → Predict
├── public/
│   ├── login.html           # Login page
│   ├── dashboard.html       # Main dashboard
│   └── dummy_data.json      # Demo data
└── functions/
    └── index.js             # Firebase Cloud Functions
```

---

## 🎯 Typical Workflow

1. **Start Flask API** (Terminal 1)
   ```bash
   source venv/bin/activate
   python3 app.py
   ```

2. **Start Frontend** (Terminal 2)
   ```bash
   cd public && python3 -m http.server 8000
   ```

3. **Push Sensor Data** (Terminal 3)
   ```bash
   python3 push_test_data.py continuous /sensor_data 3
   ```

4. **Open Dashboard** 
   - Go to: http://localhost:8000/login.html
   - Login/Signup
   - Watch live data update!

---

## 🚀 Next Steps

- [ ] Configure real IoT sensors (ESP32/Arduino)
- [ ] Deploy to Firebase Hosting
- [ ] Add email/SMS alerts
- [ ] Train custom ML model
- [ ] Add more sensor types

---

**Need Help?** Check `README.md` for detailed documentation

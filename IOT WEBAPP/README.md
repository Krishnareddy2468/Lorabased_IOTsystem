# SmartAgro - IoT Precision Farming Dashboard

An intelligent IoT-based agriculture monitoring system with real-time sensor data tracking, AI-powered irrigation predictions, and a beautiful web dashboard.

## Features

- **Real-time Sensor Monitoring**: Track soil moisture, temperature, humidity, light, pH, and rainfall
- **AI Irrigation Predictions**: Machine learning model predicts optimal irrigation timing
- **Firebase Integration**: Real-time database and cloud functions
- **Responsive Dashboard**: Beautiful, modern web interface with live charts
- **Multi-source Data**: Supports both Firebase Realtime Database and REST API

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- Firebase project with:
  - Realtime Database enabled
  - Firestore enabled
  - Cloud Functions enabled (optional for deployment)
- Firebase service account key JSON file

## Quick Start

### 1. Clone and Setup

```bash
cd "IOT WEBAPP"
```

### 2. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing: `agrivision-1e11f`
3. Enable Realtime Database and Firestore
4. Download service account key:
   - Project Settings → Service Accounts → Generate New Private Key
   - Save as `serviceAccountKey.json` in project root

### 3. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies

```bash
# Root package (optional)
npm install

# Firebase Functions
cd functions
npm install
cd ..
```

## Running the Application

### Option 1: Local Development (Recommended for Testing)

#### Start Flask API Server

```bash
# Activate virtual environment if not already
source venv/bin/activate

# Run Flask API on port 5001
python3 app.py
```

The Flask API will be available at `http://127.0.0.1:5001`

#### Serve Frontend Locally

```bash
# In a new terminal, serve the public directory
cd public
python3 -m http.server 8000
```

Open your browser to `http://localhost:8000/login.html`

### Option 2: Firebase Hosting (Production)

```bash
# Install Firebase CLI if not already installed
npm install -g firebase-tools

# Login to Firebase
firebase login

# Deploy hosting and functions
firebase deploy
```

## Usage Guide

### Testing the System

#### 1. Push Test Data to Firebase

```bash
# Push a single sensor reading
python3 push_test_data.py once

# Push data continuously every 5 seconds
python3 push_test_data.py continuous /sensor_data 5

# Push 10 readings then stop
python3 push_test_data.py continuous /sensor_data 2 10

# Push historical data
python3 push_test_data.py historical /historical_data 20
```

#### 2. Fetch Data and Get Predictions

Make sure Flask API is running first!

```bash
# Fetch once and predict
python3 fetch_and_predict.py once

# Listen continuously (polls every 5 seconds)
python3 fetch_and_predict.py listen /sensor_data 5

# Custom database path
python3 fetch_and_predict.py once /custom_path
```

#### 3. Direct API Testing

```bash
# Test API health
curl http://127.0.0.1:5001/

# Send prediction request
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

### Using the Dashboard

1. **Login/Signup**: 
   - Open `http://localhost:8000/login.html`
   - Create account or login (stored in browser localStorage)

2. **View Live Data**:
   - Dashboard automatically cycles through demo data
   - Real Firebase data will be shown if available

3. **Monitor Predictions**:
   - AI predictions update in real-time
   - Alerts show when irrigation is needed

## Project Structure

```
IOT WEBAPP/
├── app.py                      # Flask API server with ML model
├── fetch_and_predict.py        # Script to fetch Firebase data → Flask API
├── push_test_data.py          # Script to push test data to Firebase
├── requirements.txt            # Python dependencies
├── irrigation_model.pkl        # Trained ML model
├── serviceAccountKey.json      # Firebase credentials (DO NOT COMMIT!)
├── firebase.json              # Firebase configuration
├── package.json               # Node.js dependencies
├── public/                    # Frontend files
│   ├── index.html            # Landing page
│   ├── login.html            # Login/Signup page
│   ├── dashboard.html        # Main dashboard
│   ├── script.js             # Firebase initialization
│   └── dummy_data.json       # Demo sensor data
└── functions/                 # Firebase Cloud Functions
    ├── index.js              # API endpoints
    └── package.json          # Function dependencies
```

## Configuration

### Flask API (`app.py`)

- **Port**: 5001 (change in `app.run()`)
- **Model**: `irrigation_model.pkl` (must be in root)
- **Firebase**: Uses `serviceAccountKey.json`

### Firebase Configuration

Update `firebase.json` as needed:

```json
{
  "hosting": {
    "public": "public",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
  },
  "functions": {
    "source": "functions"
  }
}
```

### Environment Variables

Create `.env` file (optional):

```bash
FLASK_PORT=5001
FIREBASE_DATABASE_URL=https://agrivision-1e11f-default-rtdb.asia-southeast1.firebasedatabase.app
```

## Testing

### Manual Testing Flow

1. **Start Flask API**: `python3 app.py`
2. **Push test data**: `python3 push_test_data.py continuous /sensor_data 3`
3. **Fetch and predict**: In another terminal: `python3 fetch_and_predict.py listen /sensor_data 5`
4. **View dashboard**: Open `http://localhost:8000/dashboard.html`

### API Endpoints

#### Flask API (`http://127.0.0.1:5001`)

- `GET /` - Health check
- `POST /predict` - Get irrigation prediction

#### Firebase Functions (after deployment)

- `GET /healthCheck` - API status
- `GET /getSensorData` - Retrieve sensor data
- `POST /storeSensorData` - Store sensor data
- `GET /getPrediction` - Get latest prediction

## Data Flow

```
IoT Sensors (ESP32/Arduino)
    ↓
Firebase Realtime Database (/sensor_data)
    ↓
fetch_and_predict.py (Python script)
    ↓
Flask API (POST /predict)
    ↓
ML Model (irrigation_model.pkl)
    ↓
Firestore (fields/field_1) ← Dashboard reads from here
    ↓
Web Dashboard (public/dashboard.html)
```

## Security Notes

⚠️ **IMPORTANT**: Never commit `serviceAccountKey.json` to version control!

Add to `.gitignore`:

```
serviceAccountKey.json
*.pkl
venv/
node_modules/
.env
*.local
```

## Troubleshooting

### Flask API not connecting

```bash
# Check if port 5001 is in use
lsof -i :5001

# Try different port
python3 app.py  # Edit app.py to change port
```

### Firebase connection errors

1. Verify `serviceAccountKey.json` is in root directory
2. Check Firebase Realtime Database URL in scripts
3. Ensure Firebase rules allow read/write

### Model not found

```bash
# Ensure irrigation_model.pkl exists
ls -la irrigation_model.pkl

# If missing, you need to train the model first
```

### Dashboard not loading data

1. Check browser console for errors (F12)
2. Verify `dummy_data.json` exists in `public/`
3. Check if Firebase is initialized correctly

## Dependencies

### Python

- Flask 3.0.0 - Web framework
- flask-cors 4.0.0 - CORS support
- firebase-admin 6.4.0 - Firebase SDK
- pandas 2.1.4 - Data processing
- scikit-learn 1.3.2 - ML model
- requests 2.31.0 - HTTP client

### Node.js

- firebase-admin 12.6.0
- firebase-functions 6.0.1

## Deployment

### Deploy to Firebase

```bash
# Build and deploy
firebase deploy

# Deploy only hosting
firebase deploy --only hosting

# Deploy only functions
firebase deploy --only functions
```

### Deploy Flask API (Cloud Run)

The `apphosting.yaml` is configured for Firebase App Hosting:

```bash
# Deploy Flask API to Cloud Run via Firebase
firebase apphosting:backends:create

# Or use Google Cloud Run directly
gcloud run deploy smartagro-api --source .
```

## License

This project is for educational and agricultural purposes.

## Contributing

Feel free to submit issues and enhancement requests!

## Support

For issues or questions:
- Check Firebase Console for database/function logs
- Review Flask terminal output for API errors
- Use browser DevTools to debug frontend issues

---

**Made with for Smart Agriculture**

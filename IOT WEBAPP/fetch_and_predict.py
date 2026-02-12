"""
Script to fetch sensor data from Firebase Realtime Database 
and send it to the Flask API for irrigation predictions.
"""

import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import json

# Initialize Firebase Admin SDK with Realtime Database
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize with the Realtime Database URL from your firebase config
# You need to specify the databaseURL
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://agrivision-1e11f-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

# Flask API endpoint
API_URL = "http://127.0.0.1:5001/predict"

def fetch_sensor_data(path='/sensor_data'):
    """
    Fetch sensor data from Firebase Realtime Database
    
    Args:
        path: The path in the database (e.g., '/sensor_data', '/field_1/sensors')
    
    Returns:
        Dictionary with sensor readings
    """
    try:
        ref = db.reference(path)
        data = ref.get()
        
        if data:
            print(f"✓ Fetched data from Firebase: {json.dumps(data, indent=2)}")
            return data
        else:
            print(f"✗ No data found at path: {path}")
            return None
            
    except Exception as e:
        print(f"✗ Error fetching from Firebase: {e}")
        return None

def send_to_prediction_api(sensor_data):
    """
    Send sensor data to Flask API for prediction
    
    Args:
        sensor_data: Dictionary containing sensor readings
    
    Returns:
        Prediction response from API
    """
    try:
        # Prepare data in the format expected by the API
        payload = {
            "soil": sensor_data.get("soil", sensor_data.get("soilMoisture", 0)),
            "light": sensor_data.get("light", sensor_data.get("lightIntensity", 0)),
            "temperature": sensor_data.get("temperature", sensor_data.get("temp", 0)),
            "humidity": sensor_data.get("humidity", 0),
            "pH": sensor_data.get("pH", sensor_data.get("ph", 7.0)),
            "npk": sensor_data.get("npk", 25),
            "rainfall": sensor_data.get("rainfall", 0)
        }
        
        print(f"\n→ Sending to API: {json.dumps(payload, indent=2)}")
        
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Prediction received:")
            print(f"  Irrigation Needed: {'YES' if result['irrigation_needed'] else 'NO'}")
            print(f"  Confidence: {result['confidence'] * 100}%")
            print(f"  Reason: {result['reason']}")
            return result
        else:
            print(f"✗ API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to Flask API. Make sure it's running on http://127.0.0.1:5001")
        return None
    except Exception as e:
        print(f"✗ Error sending to API: {e}")
        return None

def listen_realtime(path='/sensor_data', interval=5):
    """
    Continuously listen for changes in Firebase Realtime Database
    and send updates to the prediction API
    
    Args:
        path: Database path to monitor
        interval: Polling interval in seconds (for simple polling)
    """
    print(f"\n🔄 Starting realtime listener on path: {path}")
    print(f"📡 Polling every {interval} seconds...")
    print("Press Ctrl+C to stop\n")
    
    last_data = None
    
    try:
        while True:
            data = fetch_sensor_data(path)
            
            # Only send to API if data exists and has changed
            if data and data != last_data:
                print("\n" + "="*60)
                print(f"📊 New sensor data detected!")
                print("="*60)
                send_to_prediction_api(data)
                last_data = data
            elif not data:
                print(f"⚠ Waiting for data at {path}...")
            else:
                print(".", end="", flush=True)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✓ Stopped listening")

def fetch_once(path='/sensor_data'):
    """
    Fetch data once and make a single prediction
    
    Args:
        path: Database path to read from
    """
    print(f"\n📥 Fetching data from Firebase Realtime Database...")
    print(f"Path: {path}\n")
    
    data = fetch_sensor_data(path)
    
    if data:
        send_to_prediction_api(data)
    else:
        print("\n⚠ No data available. Make sure:")
        print("  1. Your Firebase Realtime Database has data at the specified path")
        print("  2. The database rules allow read access")
        print("  3. The databaseURL is correct")

if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("  Firebase Realtime Database → Flask Prediction API")
    print("="*60)
    
    # Check if Flask API is running
    try:
        test_response = requests.get("http://127.0.0.1:5001/", timeout=2)
        print("✓ Flask API is running\n")
    except:
        print("⚠ WARNING: Flask API doesn't seem to be running!")
        print("  Start it with: python3 app.py\n")
    
    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else "once"
    db_path = sys.argv[2] if len(sys.argv) > 2 else "/sensor_data"
    
    if mode == "listen":
        # Continuous monitoring mode
        interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        listen_realtime(db_path, interval)
    else:
        # Fetch once mode (default)
        fetch_once(db_path)
    
    print("\n" + "="*60)

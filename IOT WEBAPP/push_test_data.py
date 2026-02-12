"""
Script to push test sensor data to Firebase Realtime Database
"""

import firebase_admin
from firebase_admin import credentials, db
import time
import random

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://agrivision-1e11f-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

def generate_sensor_data():
    """Generate random sensor data for testing"""
    return {
        "soil": random.randint(100, 900),
        "light": random.randint(100, 1000),
        "temperature": round(random.uniform(15, 40), 1),
        "humidity": round(random.uniform(20, 90), 1),
        "pH": round(random.uniform(5.0, 8.0), 1),
        "npk": random.randint(10, 50),
        "rainfall": round(random.uniform(0, 100), 1),
        "timestamp": int(time.time() * 1000)
    }

def push_single_data(path='/sensor_data'):
    """Push a single sensor reading to Firebase"""
    data = generate_sensor_data()
    
    print(f"\n📤 Pushing data to Firebase Realtime Database")
    print(f"Path: {path}")
    print(f"Data: {data}\n")
    
    try:
        ref = db.reference(path)
        ref.set(data)
        print("✓ Data pushed successfully!")
        return data
    except Exception as e:
        print(f"✗ Error pushing data: {e}")
        return None

def push_continuous(path='/sensor_data', interval=5, count=None):
    """
    Continuously push sensor data to Firebase
    
    Args:
        path: Database path
        interval: Time between pushes in seconds
        count: Number of pushes (None for infinite)
    """
    print(f"\n🔄 Starting continuous data push")
    print(f"Path: {path}")
    print(f"Interval: {interval} seconds")
    print(f"Count: {'Infinite' if count is None else count}")
    print("Press Ctrl+C to stop\n")
    
    pushed = 0
    
    try:
        while count is None or pushed < count:
            data = generate_sensor_data()
            
            try:
                ref = db.reference(path)
                ref.set(data)
                pushed += 1
                
                print(f"[{pushed}] ✓ Pushed: soil={data['soil']}, temp={data['temperature']}°C, humidity={data['humidity']}%")
                
                if count and pushed >= count:
                    break
                    
                time.sleep(interval)
                
            except Exception as e:
                print(f"✗ Error: {e}")
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print(f"\n\n✓ Stopped after {pushed} pushes")

def push_historical_data(path='/historical_data', count=10):
    """Push multiple historical sensor readings"""
    print(f"\n📚 Pushing {count} historical records to {path}")
    
    try:
        ref = db.reference(path)
        
        for i in range(count):
            data = generate_sensor_data()
            ref.child(str(int(time.time() * 1000) + i)).set(data)
            print(f"[{i+1}/{count}] ✓ Pushed record")
            time.sleep(0.1)
        
        print(f"\n✓ Successfully pushed {count} historical records!")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("  Push Sensor Data to Firebase Realtime Database")
    print("="*60)
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "once"
    
    if mode == "once":
        # Push single reading
        path = sys.argv[2] if len(sys.argv) > 2 else "/sensor_data"
        push_single_data(path)
        
    elif mode == "continuous":
        # Continuous push
        path = sys.argv[2] if len(sys.argv) > 2 else "/sensor_data"
        interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        count = int(sys.argv[4]) if len(sys.argv) > 4 else None
        push_continuous(path, interval, count)
        
    elif mode == "historical":
        # Push historical data
        path = sys.argv[2] if len(sys.argv) > 2 else "/historical_data"
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        push_historical_data(path, count)
        
    else:
        print("\nUsage:")
        print("  python3 push_test_data.py once [path]")
        print("  python3 push_test_data.py continuous [path] [interval] [count]")
        print("  python3 push_test_data.py historical [path] [count]")
        print("\nExamples:")
        print("  python3 push_test_data.py once")
        print("  python3 push_test_data.py continuous /sensor_data 5")
        print("  python3 push_test_data.py continuous /sensor_data 2 10")
        print("  python3 push_test_data.py historical /historical_data 20")
    
    print("\n" + "="*60)

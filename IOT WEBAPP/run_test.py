import requests
import time

# Wait a moment for the server to be ready
time.sleep(1)

# URL of your running Flask API
url = "http://127.0.0.1:5001/predict"

# Sample sensor data
data = {
    "soil": 200,
    "light": 300,
    "temperature": 37,
    "humidity": 30,
    "pH": 7.0,
    "rainfall": 5
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    try:
        print("\nResponse JSON:", response.json())
    except Exception as e:
        print("Failed to parse JSON:", e)
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to Flask server. Make sure it's running on http://127.0.0.1:5000")
except Exception as e:
    print(f"Error: {e}")

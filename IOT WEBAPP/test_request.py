import requests

# URL of your running Flask API
url = "http://127.0.0.1:5000/predict"

# Sample sensor data
data = {
    "soil": 200,
    "light": 300,
    "temperature": 37,
    "humidity": 30,
    "pH": 7.0,
    "rainfall": 5
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Failed to parse JSON:", e)
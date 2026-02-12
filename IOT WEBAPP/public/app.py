from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import pickle
import pandas as pd
from flask_cors import CORS

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load model and scaler
try:
    with open("irrigation_model.pkl", "rb") as f:
        model_data = pickle.load(f)
        if isinstance(model_data, dict):
            model = model_data["model"]
            scaler = model_data["scaler"]
        else:
            # Old format - just the model
            model = model_data
            scaler = None
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = None

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running! Use POST /predict to get predictions."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
            
        data = request.json
        # Create DataFrame with expected feature order
        df = pd.DataFrame([{
            "soil": data.get("soil"),
            "light": data.get("light"),
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "pH": data.get("pH"),
            "npk": data.get("npk", 25),  # Default value if not provided
            "rainfall": data.get("rainfall")
        }])
        
        # Scale if scaler is available
        if scaler is not None:
            df_scaled = scaler.transform(df)
            prediction = int(model.predict(df_scaled)[0])
            confidence = round(float(model.predict_proba(df_scaled).max()), 2)
        else:
            prediction = int(model.predict(df)[0])
            confidence = round(float(model.predict_proba(df).max()), 2)
            
        if data['soil'] < 250 and data['humidity'] < 40:
            reason = "Low soil moisture and low humidity"
        elif data['rainfall'] < 10:
            reason = "Low rainfall levels"
        else:
            reason = "Good moisture condition"
        result = {
            "irrigation_needed": prediction,
            "confidence": confidence,
            "reason": reason
        }
        try:
            db.collection("fields").document("field_1").set({
                "Soil": data.get("soil"),
                "Light": data.get("light"),
                "Temperature": data.get("temperature"),
                "Humidity": data.get("humidity"),
                "pH": data.get("pH"),
            
                "Rainfall": data.get("rainfall"),
                "irrigation_needed": prediction,
                "Confidence": confidence,
                "Reason": reason
            }, merge=True)
        except Exception as firestore_error:
            print("Firestore Error:", firestore_error)
            # Don't return error - just log it
            pass
        return jsonify(result)
    except Exception as e:
        print("Prediction Error:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5001)
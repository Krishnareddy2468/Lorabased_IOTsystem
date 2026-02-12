from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS
import os

# Firebase initialization (optional - gracefully handle if credentials missing)
db = None
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if os.path.exists("serviceAccountKey.json"):
        # Check if it's a real key (not template)
        with open("serviceAccountKey.json", "r") as f:
            import json
            key_data = json.load(f)
            if "REPLACE" not in key_data.get("private_key", ""):
                cred = credentials.Certificate("serviceAccountKey.json")
                firebase_admin.initialize_app(cred)
                db = firestore.client()
                print("✓ Firebase initialized successfully!")
            else:
                print("⚠ Using template serviceAccountKey.json - Firebase features disabled")
                print("  Download real credentials from Firebase Console to enable cloud features")
    else:
        print("⚠ serviceAccountKey.json not found - Firebase features disabled")
except Exception as e:
    print(f"⚠ Firebase initialization skipped: {e}")
    print("  App will work in standalone mode without cloud storage")

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
        print(f"\n📥 Received prediction request: {data}")
        
        # Create DataFrame with expected feature order (WITH rainfall - using 0 as default)
        df = pd.DataFrame([{
            "soil": data.get("soil"),
            "light": data.get("light"),
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "pH": data.get("pH"),
            "npk": data.get("npk", 25),  # Default value if not provided
            "rainfall": data.get("rainfall", 0)  # Default to 0 if not provided
        }])
        
        print(f"📊 DataFrame for prediction:\n{df}")
        
        # Scale if scaler is available
        if scaler is not None:
            df_scaled = scaler.transform(df)
            model_prediction = int(model.predict(df_scaled)[0])
            confidence = round(float(model.predict_proba(df_scaled).max()), 2)
        else:
            model_prediction = int(model.predict(df)[0])
            confidence = round(float(model.predict_proba(df).max()), 2)
            
        # CRITICAL: Override model if soil moisture is dangerously low
        # Soil moisture values: 0-400 (0 = very dry, 400+ = waterlogged)
        # Threshold: Below 300 needs irrigation
        if data['soil'] < 300:
            prediction = 1  # Force irrigation needed
            if data['soil'] < 100:
                reason = f"CRITICAL: Very low soil moisture ({data['soil']}) - immediate irrigation required"
            else:
                reason = f"Low soil moisture ({data['soil']}) - irrigation required"
            confidence = 0.95  # High confidence for manual override
            print(f"⚠️ OVERRIDE: Soil={data['soil']} is below 300 threshold, forcing irrigation=1")
        else:
            prediction = model_prediction
            # Enhanced reasoning based on actual sensor values
            if data['humidity'] < 30:
                reason = "Low humidity - monitor soil moisture closely"
            else:
                reason = "Good moisture levels - no irrigation needed"
            
        print(f"🤖 Final Prediction: {prediction}, Confidence: {confidence}, Reason: {reason}")
        
        result = {
            "irrigation_needed": prediction,
            "confidence": confidence,
            "reason": reason
        }
        
        # Save to Firestore if available
        if db is not None:
            try:
                db.collection("fields").document("field_1").set({
                    "Soil": data.get("soil"),
                    "Light": data.get("light"),
                    "Temperature": data.get("temperature"),
                    "Humidity": data.get("humidity"),
                    "pH": data.get("pH"),
                    "Rainfall": data.get("rainfall", 0),
                    "irrigation_needed": prediction,
                    "Confidence": confidence,
                    "Reason": reason
                }, merge=True)
                print("✓ Data saved to Firestore")
            except Exception as firestore_error:
                print("⚠ Firestore Error:", firestore_error)
        else:
            print("ℹ Firestore not configured - prediction not saved to cloud")
            
        return jsonify(result)
    except Exception as e:
        print("Prediction Error:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5001)
# 🌾 AgriVision — LoRa-Based Smart IoT Precision Farming System

> An end-to-end IoT solution for precision agriculture using **LoRa wireless communication**, **ESP32 microcontrollers**, **AI-powered irrigation prediction**, and a **real-time Firebase-connected web dashboard**.

---

## Overview

AgriVision is a complete smart agriculture system that collects real-time environmental sensor data from remote field nodes, transmits it over **long-range LoRa radio**, processes it through an **AI/ML irrigation model**, and displays actionable insights on a **live web dashboard**.

### Key Highlights

- 🛰️ **LoRa Communication** — Long-range (up to 10+ km), low-power wireless data transmission between field nodes
- 🧠 **AI Irrigation Prediction** — Trained ML model predicts optimal irrigation timing based on sensor data
- 🔥 **Firebase Integration** — Real-time database, Firestore, and Cloud Functions for cloud-native data flow
- 📊 **Live Dashboard** — Real-time charts, sensor monitoring, and prediction alerts
- ⚙️ **Modular Hardware Design** — Separate sensor, forest (transmitter), and ground (receiver) nodes

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FIELD DEPLOYMENT                             │
│                                                                     │
│  ┌──────────────┐    LoRa     ┌──────────────┐    WiFi              │
│  │ Sensor Node  │ ─────────▶ │ Ground Node  │ ──────────▶ Internet │
│  │ (ESP32 +     │  915 MHz    │ (ESP32 +     │                      │
│  │  DHT11, LDR, │             │  LoRa RX +   │                      │
│  │  Soil, pH)   │             │  WiFi)       │                      │
│  └──────────────┘             └──────┬───────┘                      │
│                                      │                              │
│  ┌──────────────┐    LoRa            │                              │
│  │ Forest Node  │ ──────────────┐    │                              │
│  │ (ESP32 TX +  │               │    │                              │
│  │  Auto Pump)  │               ▼    ▼                              │
│  └──────────────┘     Firebase Realtime Database                    │
│                                      │                              │
└──────────────────────────────────────┼──────────────────────────────┘
                                       │
                        ┌──────────────┼──────────────┐
                        │         CLOUD LAYER          │
                        │                              │
                        │  Firebase RTDB ──▶ Flask API │
                        │                   (ML Model) │
                        │                      │       │
                        │              Firestore DB    │
                        │                      │       │
                        │              Web Dashboard   │
                        └──────────────────────────────┘
```

---

## 📸 Project Gallery

### 🧠 ML Model Performance

#### 3D ROC Curves — AUC Comparison
![3D ROC Curves with AUC Regions](docs/images/results/roc_curves_3d_auc.png)
*ROC curves comparing Random Forest (0.834), XGBoost (0.838), Gradient Boosting (0.837), and LightGBM (0.831) for soil moisture irrigation prediction*

#### Multi-Metric Model Comparison
| Performance Flow | Radar Chart |
|:---:|:---:|
| ![3D Ribbon Chart](docs/images/results/ribbon_chart_performance.png) | ![3D Radar Chart](docs/images/results/radar_chart_model_comparison.png) |
| *Performance across Accuracy, Precision, Recall, F1-Score, ROC-AUC* | *Multi-metric comparison across all 4 models* |

#### Feature Importance Analysis
![Feature Importance 3D Mesh](docs/images/results/feature_importance_3d_mesh.png)
*3D Mesh Surface showing feature importance (Soil Moisture, Temperature, Humidity, pH, Light) across Random Forest, XGBoost, Gradient Boosting, and LightGBM*

### 📡 LoRa Communication Analysis

| Packet Delivery Performance | Signal Coverage Map |
|:---:|:---:|
| ![LoRa PDR Mesh](docs/images/results/lora_packet_delivery_mesh.png) | ![LoRa Coverage Map](docs/images/results/lora_signal_coverage_map.png) |
| *3D Link Quality: PDR vs Distance & Spreading Factor* | *3D Terrain Coverage: Signal distribution from gateway* |

### 🔧 Hardware Setup
<!-- Add your hardware photos here -->
| | |
|:---:|:---:|
| *ESP32 Forest Node — Add photo* | *Ground Node Gateway — Add photo* |
| *Sensor Connections — Add photo* | *Full System Setup — Add photo* |

### 💻 Dashboard Screenshots
<!-- Add your dashboard screenshots here -->

---

## 🔧 Hardware Components

| Component | Purpose | Pin Configuration |
|-----------|---------|-------------------|
| **ESP32 DevKit** | Main microcontroller | SPI: SCK=18, MISO=19, MOSI=23 |
| **LoRa SX1276/78** | Long-range communication (915 MHz) | SS=5, RST=14, DIO0=2 |
| **DHT11** | Temperature & Humidity sensor | GPIO 4 |
| **Soil Moisture Sensor** | Soil moisture level (analog) | GPIO 36 |
| **LDR Sensor** | Light intensity detection | GPIO 32 |
| **pH Sensor** | Soil pH level (analog) | GPIO 33 |
| **Relay Module** | Automated pump control | GPIO 15 |

---

## 📂 Project Structure

```
LoraBased_IOTsystem/
│
├── 📁 docs/                         # Documentation & Media
│   └── 📁 images/                   #   Project images & photos
│       ├── 📁 hardware/             #     Circuit & sensor photos
│       ├── 📁 dashboard/            #     Dashboard screenshots
│       ├── 📁 architecture/         #     System diagrams
│       ├── 📁 demo/                 #     Demo day photos
│       └── 📁 results/              #     ML results & graphs
│
├── 📁 ESP32_Forestnode/             # LoRa Transmitter Node (Field)
│   └── ESP32_Forestnode.ino         #   Reads sensors, controls pump, sends via LoRa
│
├── 📁 ground_node/                  # LoRa Receiver Node (Gateway)
│   └── ground_node.ino             #   Receives LoRa data, uploads to Firebase RTDB
│
├── 📁 sensor_node/                  # Standalone Sensor Node
│   └── sensor_node.ino             #   Basic sensor reading + LoRa transmission
│
├── 📁 IOT WEBAPP/                   # Web Application & ML Backend
│   ├── app.py                       #   Flask API server with ML model inference
│   ├── fetch_and_predict.py         #   Fetches Firebase data → sends to Flask API
│   ├── push_test_data.py            #   Push simulated sensor data for testing
│   ├── irrigation_model.pkl         #   Trained scikit-learn irrigation model
│   ├── requirements.txt             #   Python dependencies
│   ├── firebase.json                #   Firebase hosting & functions config
│   ├── apphosting.yaml              #   Firebase App Hosting config
│   ├── .env.example                 #   Environment variables template
│   ├── serviceAccountKey.json.template  # Firebase credentials template
│   │
│   ├── 📁 public/                   #   Frontend Dashboard
│   │   ├── index.html               #     Main dashboard with live charts
│   │   ├── 404.html                 #     Error page
│   │   └── dummy_data.json          #     Demo data for offline testing
│   │
│   └── 📁 functions/                #   Firebase Cloud Functions
│       ├── index.js                 #     API endpoints (health, store, predict)
│       └── package.json             #     Node.js dependencies
│
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 📊 Data Flow Pipeline

```
1. SENSE     →  ESP32 reads DHT11, Soil Moisture, LDR, pH sensors
2. TRANSMIT  →  Data encoded as CSV string, sent via LoRa @ 915 MHz
3. RECEIVE   →  Ground node receives LoRa packet via SPI
4. UPLOAD    →  Ground node pushes data to Firebase Realtime Database
5. FETCH     →  Python script polls Firebase for new readings
6. PREDICT   →  Flask API runs ML model (scikit-learn) on sensor data
7. STORE     →  Prediction results saved to Firestore
8. DISPLAY   →  Web dashboard renders live charts & irrigation alerts
```

---

## 🧠 AI/ML Irrigation Model

The system uses a **scikit-learn** classification model trained on agricultural sensor data:

| Feature | Range | Description |
|---------|-------|-------------|
| Soil Moisture | 0–4095 | Analog reading (low = dry) |
| Light | 0–4095 | LDR analog reading |
| Temperature | 0–50°C | Ambient temperature |
| Humidity | 0–100% | Relative humidity |
| pH | 0–14 | Soil acidity/alkalinity |
| NPK | 0–100 | Nutrient levels |
| Rainfall | 0–500mm | Precipitation |

**Smart Override Logic**: If soil moisture drops below 300, the system automatically overrides the ML prediction and triggers irrigation — ensuring critical conditions are never missed.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Krishnareddy2468/Lorabased_IOTsystem.git
cd Lorabased_IOTsystem
```

### 2. Hardware Setup

Flash the Arduino `.ino` files to your ESP32 boards:
- `ESP32_Forestnode/ESP32_Forestnode.ino` → Field transmitter node
- `ground_node/ground_node.ino` → Gateway receiver node
- `sensor_node/sensor_node.ino` → Additional sensor node (optional)

### 3. Web App Setup

```bash
cd "IOT WEBAPP"

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Firebase (download your serviceAccountKey.json)
# See: Firebase Console → Project Settings → Service Accounts

# Start Flask API
python3 app.py
```

### 4. Run the Dashboard

```bash
# In a separate terminal
cd "IOT WEBAPP/public"
python3 -m http.server 8000
```

Open `http://localhost:8000` to view the live dashboard.

### 5. Test with Simulated Data

```bash
# Push test sensor data to Firebase
python3 push_test_data.py continuous /sensor_data 5

# Fetch and run predictions
python3 fetch_and_predict.py listen /sensor_data 5
```

---

## 🔌 API Endpoints

### Flask API (`http://127.0.0.1:5001`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict` | Submit sensor data, get irrigation prediction |

### Firebase Cloud Functions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/healthCheck` | API status |
| `GET` | `/getSensorData` | Retrieve latest sensor data |
| `POST` | `/storeSensorData` | Store new sensor reading |
| `GET` | `/getPrediction` | Get latest ML prediction |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Microcontroller** | ESP32 DevKit V1 |
| **Communication** | LoRa SX1276 (915 MHz, SF12, BW 125kHz) |
| **Sensors** | DHT11, Capacitive Soil Moisture, LDR, pH Sensor |
| **Backend** | Python 3.8+, Flask, scikit-learn, pandas |
| **Database** | Firebase Realtime Database, Cloud Firestore |
| **Cloud Functions** | Node.js 18, Firebase Functions |
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Hosting** | Firebase Hosting / Cloud Run |

---

## 🔐 Security

- `serviceAccountKey.json` is **never committed** — use the `.template` version as reference
- Firebase database rules configured in `database.rules.json`
- Firestore security rules in `firestore.rules`
- Environment variables stored in `.env` (not committed)

---

## 📄 License

This project is built for educational and agricultural research purposes.

---

<p align="center">
  <b>🌱 Built with passion for Smart Agriculture & IoT 🌱</b><br>
  <i>AgriVision — Making farming smarter, one sensor at a time</i>
</p>

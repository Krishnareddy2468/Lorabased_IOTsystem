# ESP32 Forest Node (Transmitter)

The Forest Node is the primary field unit responsible for collecting environmental data and controlling the irrigation system. It reads data from multiple sensors and transmits it via LoRa to the Ground Node (Gateway).

## Features

- **Multi-Sensor Monitoring**: Reads Temperature, Humidity, Soil Moisture, Light intensity (LDR), and pH levels.
- **Smart Irrigation Control**: Automatically triggers a water pump when soil moisture falls below a specific threshold.
- **LoRa Transmission**: Sends sensor data payloads wirelessly over long distances (915 MHz).
- **Power Efficient**: Designed for deep sleep integration (future scope).

## Hardware Configuration

| Component | Pin (ESP32) | Notes |
|-----------|-------------|-------|
| **LoRa SX1276/78** | SPI (VSPI) | standard module with NSS, RST, DIO0 |
| NSS (CS) | GPIO 5 | Chip Select |
| RST | GPIO 14 | Reset |
| DIO0 | GPIO 2 | Interrupt |
| SCK | GPIO 18 | SPI Clock |
| MISO | GPIO 19 | SPI MISO |
| MOSI | GPIO 23 | SPI MOSI |
| **DHT11** | GPIO 4 | Temperature & Humidity |
| **Soil Moisture** | GPIO 36 (VP) | Analog Input (Capacitive) |
| **LDR Sensor** | GPIO 32 | Digital/Analog Light Sensor |
| **pH Sensor** | GPIO 33 | Analog Input |
| **Pump Relay** | GPIO 15 | Active High/Low Control |

## Logic Flow

1. **Initialize**: Setup Serial, DHT sensor, Relay, and LoRa radio.
2. **Read Sensors**: Collect data from all connected sensors.
3. **Pump Control**:
    - If `Moisture < Threshold` (e.g., 400), Turn Pump ON.
    - Else, Turn Pump OFF.
4. **Create Payload**: Format data as a string: `humidity:50.0,temperature:25.0,moisture:1024,pH:6.5,light:Sunny`.
5. **Transmit**: Send the payload string via LoRa.
6. **Sleep/Delay**: Wait for 15 seconds before the next cycle.

## Setup Instructions

1. Install the required libraries in Arduino IDE:
    - `LoRa` by Sandeep Mistry
    - `DHT sensor library` by Adafruit
2. Select Board: `ESP32 Dev Module`.
3. Verify pin mappings match your wiring.
4. Upload the code.

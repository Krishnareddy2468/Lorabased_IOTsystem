# Standalone Sensor Node

This is a secondary sensor node designed to expand the monitoring coverage of the system. It collects basic environmental data and transmits it to the central gateway via LoRa.

## Features

- **Basic Environmental Monitoring**: Reads Soil Moisture and Light levels.
- **Extended Telemetry**: Simulates additional metrics (Temperature, Humidity, pH, NPK, Rainfall) for system testing and demonstration.
- **Long-Range Communication**: Transmits data packets using 915 MHz LoRa.

## Hardware Configuration

| Component | Pin (ESP32) | Notes |
|-----------|-------------|-------|
| **LoRa SX1276/78** | SPI | Standard connection |
| NSS (CS) | GPIO 5 | Chip Select |
| RST | GPIO 14 | Reset |
| DIO0 | GPIO 2 | Interrupt |
| **Soil Moisture** | GPIO 34 | Analog Input |
| **Light Sensor** | GPIO 35 | Analog Input |

## Operation

The node operates in a loop:
1. **Wake**: Initializes LoRa radio and Serial communication.
2. **Sense**: Reads analog values from physical sensors.
3. **Simulate**: Generates dummy values for missing sensors (Temp, Hum, NPK) to maintain packet format compatibility with the main system.
4. **Pack**: Formats data into a comma-separated string: `soil:1024,light:200,temp:25.0,...`
5. **Send**: Transmits the packet via LoRa.
6. **Wait**: Sleeps for 60 seconds before the next reading.

## Usage

This node is useful for:
- Testing the LoRa gateway's ability to handle multiple nodes.
- Monitoring areas where full pump control is not required, only data collection.

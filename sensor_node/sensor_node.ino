#include <SPI.h>
#include <LoRa.h>

// Define LoRa pins (adjust based on your wiring)
#define SS_PIN    5    // LoRa radio chip select
#define RST_PIN   14   // LoRa radio reset
#define DIO0_PIN  2    // LoRa radio DIO0

// Define sensor pins (modify based on your sensor connections)
#define SOIL_MOISTURE_PIN 34  
#define LIGHT_SENSOR_PIN 35     

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Sensor Node Starting...");

  // Initialize LoRa module at 915 MHz (adjust frequency if needed)
  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);
  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa init failed. Please check your connections.");
    while (1);
  }
  Serial.println("LoRa init succeeded.");
}

void loop() {
  // Read sensor values
  int soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  int lightLevel = analogRead(LIGHT_SENSOR_PIN);

  // Dummy sensor values for demonstration
  float temperature = 25.0;  // e.g., from a temperature sensor
  float humidity = 50.0;     // e.g., from a humidity sensor
  float pH = 6.5;            // e.g., from a soil pH sensor
  float npk = 20.0;          // e.g., from an NPK sensor
  float rainfall = 0.0;      // e.g., from a rainfall sensor
  
  // Create payload (comma-separated string)
  String payload = String("soil:") + soilMoisture + 
                   ",light:" + lightLevel + 
                   ",temp:" + temperature + 
                   ",humidity:" + humidity + 
                   ",pH:" + pH + 
                   ",npk:" + npk + 
                   ",rainfall:" + rainfall;
  
  Serial.print("Sending payload: ");
  Serial.println(payload);
  
  // Send payload via LoRa
  LoRa.beginPacket();
  LoRa.print(payload);
  LoRa.endPacket();

  delay(60000); // Wait 60 seconds before next reading
}

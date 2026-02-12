// ======================= SENSOR NODE (RECEIVER) =======================
#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"
#include <SPI.h>
#include <LoRa.h>

// ================= WiFi Configuration =================
#define WIFI_SSID "RASPI"
#define WIFI_PASSWORD "12345678"

// =============== Firebase Configuration ===============
#define API_KEY "AIzaSyDEl-pqGkOamQM5827f0VYFsXb9uyRR_qw"
#define DATABASE_URL "https://agrivision-1e11f-default-rtdb.asia-southeast1.firebasedatabase.app/"

// ================ LoRa Configuration ==================
#define LORA_SCK 18
#define LORA_MISO 19
#define LORA_MOSI 23
#define LORA_SS 5
#define LORA_RST 14
#define LORA_DIO0 2
#define LORA_SYNC_WORD 0xF3

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;
bool signupOK = false;

void setup() {
  Serial.begin(115200);

  // Initialize LoRa
  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  LoRa.setSyncWord(LORA_SYNC_WORD);
  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();
  Serial.println("LoRa initialized.");

  // Connect to WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());

  // Configure Firebase
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  config.token_status_callback = tokenStatusCallback;
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase sign-up successful.");
    signupOK = true;
  } else {
    Serial.printf("Firebase sign-up failed: %s\n", config.signer.signupError.message.c_str());
  }
  Firebase.begin(&config, &auth);
  Firebase.reconnectNetwork(true);
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String incoming = "";
    while (LoRa.available()) {
      incoming += (char)LoRa.read();
    }

    Serial.println("Received: " + incoming);

    if (signupOK && Firebase.ready()) {
      String path = "/sensor_data/" + String(millis());
      if (Firebase.RTDB.setString(&fbdo, path, incoming)) {
        Serial.println("Data uploaded to Firebase successfully.");
      } else {
        Serial.printf("Firebase upload failed: %s\n", fbdo.errorReason().c_str());
      }
    }
  }
  delay(10);
}

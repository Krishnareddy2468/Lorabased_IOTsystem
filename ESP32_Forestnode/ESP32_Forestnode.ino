// ======================= FOREST NODE (TRANSMITTER) =======================
#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define LORA_SS 5
#define LORA_RST 14
#define LORA_DIO0 2
#define SCK 18
#define MISO 19
#define MOSI 23
#define LORA_SYNC_WORD 0xF3


#define MOISTURE_SENSOR 36
#define LDR_SENSOR 32
#define PH_SENSOR 33
#define PUMP_RELAY 15

const int moistureThreshold = 400;
const float pHCalibrationOffset = 0.0;

struct SensorData {
  float humidity;
  float temperature;
  int moisture;
  float pH;
  String light;
};

SensorData readSensors();
bool controlPump(int moisture);
String createPayload(const SensorData& data);
void sendLoRaData(String payload);
float readpH(int raw);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(PUMP_RELAY, OUTPUT);
  digitalWrite(PUMP_RELAY, LOW);
  pinMode(LDR_SENSOR, INPUT);

  SPI.begin(SCK, MISO, MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }

  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.setSyncWord(LORA_SYNC_WORD);
  LoRa.enableCrc();

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  Serial.println("LoRa Sensor Node Ready!");
}

void loop() {
  SensorData data = readSensors();
  bool pumpState = controlPump(data.moisture);
  String payload = createPayload(data);
  sendLoRaData(payload);
  delay(15000);
}

SensorData readSensors() {
  SensorData data;
  data.humidity = dht.readHumidity();
  data.temperature = dht.readTemperature();
  if (isnan(data.humidity) || isnan(data.temperature)) {
    data.humidity = 0;
    data.temperature = 0;
  }
  data.moisture = analogRead(MOISTURE_SENSOR);
  data.pH = readpH(analogRead(PH_SENSOR));
  data.light = (digitalRead(LDR_SENSOR) == LOW) ? "Sunny" : "Dark";
  return data;
}

bool controlPump(int moisture) {
  bool state = (moisture > moistureThreshold);
  digitalWrite(PUMP_RELAY, state ? HIGH : LOW);
  return state;
}

String createPayload(const SensorData& data) {
  return String() +
    "humidity:" + String(data.humidity, 1) +
    ",temperature:" + String(data.temperature, 1) +

    ",moisture:" + String(data.moisture) +
    ",pH:" + String(data.pH, 2) +
    ",light:" + data.light;
}

void sendLoRaData(String payload) {
  LoRa.beginPacket();
  LoRa.print(payload);
  LoRa.endPacket();
  Serial.println("Sent: " + payload);
}

float readpH(int raw) {
  float voltage = raw * (3.3 / 4095.0);
  return 7.0 + ((voltage - 1.5) / 0.18) + pHCalibrationOffset;
}

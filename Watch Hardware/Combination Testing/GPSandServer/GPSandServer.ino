#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPSPlus.h>

// === GPS config ===
static const int RXPin = 25;
static const int TXPin = 27;
static const uint32_t GPSBaud = 9600;
HardwareSerial gpsSerial(1);
TinyGPSPlus gps;

// === WiFi config ===
const char* ssid     = "Bedroom";
const char* password = "Gulledge134";

// === Server config ===
// For example "http://192.168.1.100:8000/location"
const char* serverURL = "http://192.168.1.69:8000/location";

void setup() {
  Serial.begin(115200);
  delay(100);
  
  // Start GPS serial
  gpsSerial.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);
  Serial.print(F("TinyGPSPlus library version: "));
  Serial.println(TinyGPSPlus::libraryVersion());

  // Connect to Wi-Fi
  Serial.printf("Connecting to WiFi %s …\n", ssid);
  WiFi.begin(ssid, password);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
    if (millis() - start > 20000) {
      Serial.println("\nFailed to connect — restarting");
      ESP.restart();
    }
  }
  Serial.println("\nWiFi connected!");
  Serial.print("  IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Feed GPS data
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  // Once we have a valid fix, send it
  if (gps.location.isValid()) {
    double lat = gps.location.lat();
    double lng = gps.location.lng();
    Serial.printf("Got fix: %.6f, %.6f\n", lat, lng);
    postLocation(lat, lng);
    // wait a bit before next post
    delay(10000);
  }

  // If no data at all after 5s, error out
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("No GPS detected: check wiring."));
    while (true) delay(1000);
  }
}

// Posts {"watch_id":"esp32_watch","lat":…, "lon":…}
void postLocation(double lat, double lon) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected, skipping POST");
    return;
  }

  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");

  // build JSON payload
  String payload = String("{") +
    "\"watch_id\":\"esp32_watch\"," +
    "\"lat\":" + String(lat, 6) + "," +
    "\"lon\":" + String(lon, 6) +
    "}";

  int httpCode = http.POST(payload);
  if (httpCode > 0) {
    Serial.printf("POST %s → %d\n", serverURL, httpCode);
    String resp = http.getString();
    Serial.println("Response: " + resp);
  } else {
    Serial.printf("POST failed, error: %s\n", http.errorToString(httpCode).c_str());
  }
  http.end();
}

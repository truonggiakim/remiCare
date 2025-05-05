#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <TinyGPSPlus.h>

// ——— Wi‑Fi & API ———
const char* SSID     = "Bedroom";
const char* PASSWORD = "Gulledge134";
const char* BASE_URL = "http://192.168.1.69:8000";

// ——— Pins ———
// GPS (UART1)
static const int GPS_RX    = 22;
static const int GPS_TX    = 27;
static const long GPS_BAUD = 9600;

// TFT (ST7789‑compatible NV3030B)
#define TFT_CS   18
#define TFT_DC   21
#define TFT_RST  27
#define TFT_BL   -1   // tied to 3.3 V

// Speaker
const int SPEAKER_PIN = 26;

// Button (manual fetch)
const int BUTTON_PIN  = 12;  // you chose GPIO12 (TDI), OK as INPUT_PULLUP

// ——— Reminders ———
static const uint32_t REM_FETCH_MS = 5UL * 60 * 1000;
struct Reminder {
  uint32_t id;
  String   text;
  uint16_t minuteOfDay;
  bool     fired;
};
std::vector<Reminder> reminders;
uint32_t lastFetch = 0;
uint8_t  lastDay   = 0xFF;

// Central Time offset UTC–6
const int8_t CT_OFF = -6;

// ——— GPS ———
HardwareSerial gpsSerial(1);
TinyGPSPlus    gps;

// ——— Display ———
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

// ——— Helpers ———
uint16_t parseTime12h(const char* s) {
  int h, m; char ap[3];
  if (sscanf(s, "%d:%d %2s", &h, &m, ap) != 3) return 0;
  if (strcmp(ap, "AM") == 0) {
    if (h == 12) h = 0;
  } else {
    if (h < 12) h += 12;
  }
  return uint16_t(h) * 60 + m;
}
uint8_t toCentral(uint8_t u) {
  int l = int(u) + CT_OFF;
  if (l < 0)      l += 24;
  else if (l >= 24) l -= 24;
  return uint8_t(l);
}

// ——— Forward declarations ———
void fetchReminders();
void sendLocation();
void checkReminders(uint16_t now);
void printStatus();
void drawReminder(const String &msg);
void drawTime(uint8_t h, uint8_t m);

void setup() {
  Serial.begin(115200);

  // GPS
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, GPS_RX, GPS_TX);

  // Speaker & Button
  pinMode(SPEAKER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Remap VSPI to your pins: SCLK=5, MISO=19, MOSI=23, SS=18
  SPI.begin(5, 19, 23, 18);

  // TFT init
  tft.init(240, 280);
  tft.setRotation(1);
  tft.fillScreen(ST77XX_BLACK);

  // Wi‑Fi connect
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Wi‑Fi…");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print('.');
  }
  Serial.println("\nConnected: " + WiFi.localIP().toString());

  // Initial fetch
  fetchReminders();
  lastFetch = millis();
}

void loop() {
  // 1) Feed GPS
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  // 2) Always send location
  sendLocation();

  // 3) Manual fetch on button
  if (digitalRead(BUTTON_PIN) == LOW) {
    fetchReminders();
    lastFetch = millis();
    delay(300);  // debounce
  }

  // 4) Periodic fetch
  if (millis() - lastFetch >= REM_FETCH_MS) {
    fetchReminders();
    lastFetch = millis();
  }

  // 5) Need valid GPS date/time
  if (!gps.date.isValid() || !gps.time.isValid()) {
    Serial.println("Waiting for GPS fix…");
    delay(1000);
    return;
  }

  // 6) Compute now in Central
  uint8_t utcH = gps.time.hour(), utcM = gps.time.minute();
  uint8_t cH   = toCentral(utcH);
  uint16_t now = uint16_t(cH)*60 + utcM;

  // 7) Midnight rollover
  uint8_t today = gps.date.day();
  if (today != lastDay) {
    for (auto &r : reminders) r.fired = false;
    lastDay = today;
  }

  // 8) Fire reminders
  checkReminders(now);

  // 9) Print status every second
  Serial.println(F("================================"));
  Serial.printf("Current Central Time: %02u:%02u\n", cH, utcM);
  printStatus();
  Serial.println(F("================================"));

  // 10) Short delay
  delay(1000);

  // 11) Redraw clock unless a reminder just fired (it drew itself)
  static uint32_t lastFireMs = 0;
  if (millis() - lastFireMs > 1000) {
    drawTime(cH, utcM);
  }
}

// ——— Implementation ———

void fetchReminders() {
  if (WiFi.status() != WL_CONNECTED) return;
  HTTPClient http;
  http.begin(String(BASE_URL) + "/reminders");
  if (http.GET() == 200) {
    String body = http.getString();
    DynamicJsonDocument doc(body.length()*1.2 + 64);
    if (!deserializeJson(doc, body) && doc.is<JsonArray>()) {
      reminders.clear();
      for (auto obj : doc.as<JsonArray>()) {
        if (!obj.containsKey("id") || !obj.containsKey("reminder") || !obj.containsKey("time"))
          continue;
        uint32_t id       = obj["id"];
        const char* text  = obj["reminder"];
        const char* tstr  = obj["time"];
        reminders.push_back({ id, String(text), parseTime12h(tstr), false });
      }
      Serial.printf("Fetched %u reminders\n", reminders.size());
    } else {
      Serial.println("❌ JSON parse error");
    }
  } else {
    Serial.printf("❌ GET failed: %d\n", http.GET());
  }
  http.end();
}

void sendLocation() {
  if (WiFi.status() != WL_CONNECTED || !gps.location.isValid()) return;
  HTTPClient http;
  http.begin(String(BASE_URL) + "/location");
  http.addHeader("Content-Type","application/json");
  String payload = String("{\"watch_id\":\"esp32_watch\",") +
                   "\"lat\":" + String(gps.location.lat(),6) +
                   ",\"lon\":" + String(gps.location.lng(),6) + "}";
  http.POST(payload);
  http.end();
}

void checkReminders(uint16_t now) {
  static uint32_t lastFireTime = 0;
  for (auto &r : reminders) {
    if (!r.fired && now >= r.minuteOfDay) {
      r.fired = true;
      Serial.printf("🔥 Fired [%u] %s\n", r.id, r.text.c_str());
      drawReminder(r.text);
      while (digitalRead(BUTTON_PIN) == HIGH) {
        tone(SPEAKER_PIN, 2000, 10);
        delay(10);
      }
      lastFireTime = millis();
    }
  }
}

void printStatus() {
  for (auto &r : reminders) {
    uint8_t h = r.minuteOfDay / 60, m = r.minuteOfDay % 60;
    Serial.printf(" • [%u] %s @ %02u:%02u → %s\n",
                  r.id, r.text.c_str(), h, m,
                  r.fired ? "FIRED" : "PENDING");
  }
}

void drawReminder(const String &msg) {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(3);
  tft.setCursor(10, 10); tft.print("Reminder:");
  tft.setTextSize(2);
  tft.setCursor(10, 60); tft.print(msg);
}

void drawTime(uint8_t h, uint8_t m) {
  char buf[6];
  snprintf(buf, sizeof(buf), "%02u:%02u", h, m);
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(4);
  tft.setCursor(10, 40); tft.print(buf);
}

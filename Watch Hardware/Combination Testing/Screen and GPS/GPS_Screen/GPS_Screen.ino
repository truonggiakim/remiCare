//using this file requires the TinyGPS and Hardware Serial library
//can not be run in vscode without specific libraries, if curious lookup projectIO
//or just use the arduino IDE. ask me if you want to mess around with them in any way
#include <TinyGPSPlus.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>


#define TFT_CS     5
#define TFT_DC     16
#define TFT_RST    17
#define TFT_BL     4  // Backlight pin (GPIO 4)

// Define the pins for GPS communication (RX, TX)
static const int RXPin = 25;  // ESP32 RX pin for GPS data
static const int TXPin = 27;  // ESP32 TX pin for GPS data, this pin is not using but is set up anyway
static const uint32_t GPSBaud = 9600; // GPS baud rate


Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);
// Create a HardwareSerial instance (use UART1 on ESP32)
HardwareSerial gpsSerial(1); // Using UART1, you can also choose UART0, UART2, etc.

// The TinyGPSPlus object
TinyGPSPlus gps;

//this code will work for most gps modules, just make sure the boad
//rate of the moduel matches what you put in
//if it is not working put it outside until it connects and then it will be able to more easily connect indoors
//this is because of the way that it can remember its last satelite it connected too

void setup()
{
  Serial.begin(115200);        // Serial monitor baud rate
  gpsSerial.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);  // Start the GPS serial communication on UART1
  Serial.print(F("Testing..... ")); Serial.println(TinyGPSPlus::libraryVersion());
  Serial.println();

  tft.init(240, 280);  // Initialize screen with width and height
  tft.setRotation(2);  // Set rotation (adjust depending on your display orientation)

  // Set the backlight
  pinMode(TFT_BL, OUTPUT);  // Set backlight pin as output
  digitalWrite(TFT_BL, HIGH);  // Set backlight to ON

  // Clear the screen with a solid background color
  tft.fillScreen(ST77XX_CYAN);  // Cyan background color

  // Display the title
  /*tft.setTextColor(ST77XX_WHITE);  // Set text color to white
  tft.setTextSize(2);  // Set text size
  String text = "Set Location";
  int textWidth = 12 * text.length();  // 12 characters, each 12 pixels wide (text size 2)
  int centerX = (240 - textWidth) / 2;  // Centering X coordinate
  // Set cursor to the center of the screen
  tft.setCursor(centerX, 20);
  tft.println(text);

  // Display the "RemiCare ;)" text
  //text = "RemiCare ;)";  // Remove comment and display
  //textWidth = 12 * text.length();  // 12 characters, each 12 pixels wide (text size 2)
  //centerX = (240 - textWidth) / 2;  // Centering X coordinate
  // Move the cursor to avoid overlap with previous text
  tft.setCursor(centerX, 60);
  tft.println("RemiCare ;)");  // Print the text

  // Display the initial location
  */
}

void loop()
{
  // This sketch displays information every time a new sentence is correctly encoded.
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      displayInfo();
    }
  }

  // If no GPS data is detected after 5 seconds, print a message and stop.
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("No GPS detected: check wiring."));
    while(true);  // Stuck here if no GPS data is received.
  }
}

void displayInfo()
{
  Serial.print(F("Location: "));
  if (gps.location.isValid()) {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
    displayLocation(gps.location.lat(), gps.location.lng());
  } else {
    Serial.print(F("INVALID"));
  }

  Serial.print(F("  Date/Time: "));
  if (gps.date.isValid()) {
    Serial.print(gps.date.month());
    Serial.print(F("/"));
    Serial.print(gps.date.day());
    Serial.print(F("/"));
    Serial.print(gps.date.year());
  } else {
    Serial.print(F("INVALID"));
  }

  Serial.print(F(" "));
  if (gps.time.isValid()) {
    if (gps.time.hour() < 10) Serial.print(F("0"));
    Serial.print(gps.time.hour());
    Serial.print(F(":"));
    if (gps.time.minute() < 10) Serial.print(F("0"));
    Serial.print(gps.time.minute());
    Serial.print(F(":"));
    if (gps.time.second() < 10) Serial.print(F("0"));
    Serial.print(gps.time.second());
    Serial.print(F("."));
    if (gps.time.centisecond() < 10) Serial.print(F("0"));
    Serial.print(gps.time.centisecond());
  } else {
    Serial.print(F("INVALID"));
  }

  Serial.println();
  delay(1000);
}

void displayLocation(double longitude, double latitude) {
  tft.fillScreen(ST77XX_CYAN);  // Cyan background color
  // Display the title
  tft.setTextColor(ST77XX_WHITE);  // Set text color to white
  tft.setTextSize(2);  // Set text size
  String text = "Set Location";
  int textWidth = 12 * text.length();  // 12 characters, each 12 pixels wide (text size 2)
  int centerX = (240 - textWidth) / 2;  // Centering X coordinate
  // Set cursor to the center of the screen
  tft.setCursor(centerX, 20);
  tft.println(text);

  tft.setCursor(centerX, 60);
  tft.println("RemiCare ;)");  // Print the text


  centerX = 48;
  tft.setCursor(centerX, 100);  // Set cursor for location display
  tft.setTextSize(2);

  tft.println("Longitude: ");
  tft.setCursor(centerX, 120);
  tft.println(longitude);  // Print the longitude
  tft.setCursor(centerX, 140);
  tft.println("Latitude: ");
  tft.setCursor(centerX, 160);
  tft.println(latitude);   // Print the latitude
}

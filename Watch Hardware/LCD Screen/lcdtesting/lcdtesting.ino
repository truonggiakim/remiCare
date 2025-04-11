#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>

// Pin definitions
#define TFT_CS     5
#define TFT_DC     16
#define TFT_RST    17
#define TFT_BL     4  // Backlight pin (GPIO 4)

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

// Placeholder for longitude and latitude
String longitude = "00000000"; // Placeholder Longitude
String latitude = "0000000";   // Placeholder Latitude

void setup() {
  Serial.begin(115200);

  // Initialize the TFT screen
  tft.init(240, 280);  // Initialize screen with width and height
  tft.setRotation(2);  // Set rotation (adjust depending on your display orientation)

  // Set the backlight
  pinMode(TFT_BL, OUTPUT);  // Set backlight pin as output
  digitalWrite(TFT_BL, HIGH);  // Set backlight to ON

  // Clear the screen with a solid background color
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

  // Display the "RemiCare ;)" text
  //text = "RemiCare ;)";  // Remove comment and display
  //textWidth = 12 * text.length();  // 12 characters, each 12 pixels wide (text size 2)
  //centerX = (240 - textWidth) / 2;  // Centering X coordinate
  // Move the cursor to avoid overlap with previous text
  tft.setCursor(centerX, 60);
  tft.println("RemiCare ;)");  // Print the text

  // Display the initial location
  displayLocation();
}

void loop() {
  // This is just a static display for now, so we don’t need to refresh the screen repeatedly.
  // You could add interactive features later if needed.

  delay(1000);  // Delay for a second before checking again
}

// Function to display location on the screen
void displayLocation(int longitude, int latitude) {
  int centerX = 48;
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

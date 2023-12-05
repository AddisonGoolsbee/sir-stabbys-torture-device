#include <WiFi.h>
#include <WiFiUdp.h>

#define TOUCH_PIN 15 

const char* ssid = "yale wireless";

const char* udpServerIP = "172.29.131.13";
const int udpServerPort = 12346;

WiFiUDP udp;

void setup() {
  Serial.begin(9600);
  delay(200);
  Serial.println("ESP32 Touch Test");

  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    Serial.println(WiFi.macAddress());
  }
  Serial.println("Connected to WiFi");

  udp.begin(udpServerPort);
}

void loop() {
  Serial.print("Touch Sensor Value on GPIO 15: ");
  Serial.println(touchRead(TOUCH_PIN));  // read the touch sensor value

  char buffer[60];
  sprintf(buffer, "Touch: %d", touchRead(TOUCH_PIN));

  Serial.println(buffer);
  udp.beginPacket(udpServerIP, udpServerPort);
  udp.println(buffer);
  udp.endPacket();
  delay(50); // delay between reads
}
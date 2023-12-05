#include <WiFi.h>
#include <WiFiUdp.h>

#define TOUCH_PIN 15 

const char* ipAddress = "172.29.131.13";
const int port = 12346;
const char* ssid = "yale wireless";

WiFiUDP udp;

void setup() {
  Serial.begin(9600);
  delay(200);

  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(WiFi.macAddress());
  }
  udp.begin(port);
}

void loop() {
  char buffer[60];
  sprintf(buffer, "Touch: %d", touchRead(TOUCH_PIN));

  Serial.println(buffer);
  udp.beginPacket(ipAddress, port);
  udp.println(buffer);
  udp.endPacket();
  delay(50);
}
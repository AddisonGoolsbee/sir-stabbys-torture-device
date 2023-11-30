#include <WiFi.h>
#include <WiFiUdp.h>
#include <math.h>
#include<Wire.h>

const int MPU_addr=0x68;  // I2C address of the MPU-6050, Plug SDA 21, SCL 22.
int16_t AcX,AcY,AcZ;
// int16_t Tmp,GyX,GyY,GyZ; // not using these, but could...

const int touchPin = 32; // nose touch sensor
const int handsPlacedPin = 33; // hands placed sensor

const char* ssid = "yale wireless";

const char* udpServerIP = "172.27.33.77";
const int udpServerPort = 12346;

WiFiUDP udp;

void setup() {
  pinMode(touchPin, INPUT);
  pinMode(handsPlacedPin, INPUT_PULLUP);
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(115200);

  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    // Serial.println("Connecting to WiFi...");
    Serial.println(WiFi.macAddress());
  }
  Serial.println("Connected to WiFi");

  udp.begin(udpServerPort);
}

void loop() {
  double touch = analogRead(touchPin) / 4096.0;
  int hands = digitalRead(handsPlacedPin);
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom((uint16_t)MPU_addr, (uint8_t)6,true);  // read 6 registers. Change to 14 for:
                                      // 6 accel, 2 temp, 6 gyro
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  float pitch = 0 + (atan2(AcX, sqrt(AcY*AcY + AcZ*AcZ)) / PI);
  float roll = 0 - (atan2(AcY, sqrt(AcX*AcX + AcZ*AcZ)) / PI);

  char buffer[60];
  sprintf(buffer, "Pitch: %.4f, Roll: %.4f, Touch: %.4f, Hands: %d", pitch, roll, touch, hands);

  Serial.println(buffer);
  udp.beginPacket(udpServerIP, udpServerPort);
  udp.println(buffer);
  udp.endPacket();
}

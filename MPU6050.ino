#include <WiFi.h>
#include <Wire.h>

const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ; 
const char* ssid = "your wifi";
const char* password = "your password";
 
WiFiServer wifiServer(80);
 
void setup()
{
  Serial.begin(115200); 
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

   wifiServer.begin();
 
}
 
void loop() {
 
  WiFiClient client = wifiServer.available();
 
  if (client) {
    Serial.print("Client connected with IP:");
    Serial.println(client.remoteIP());
 
    while (client.connected()) {
        Wire.beginTransmission(MPU_addr);
        Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
        Wire.endTransmission(false);
        Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
        AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
        AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
        AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
        client.print(AcX);
        client.print(" ");
        client.print(AcY);
        client.print(" ");
        client.println(AcZ);
        //Serial.print(AcX);
        //Serial.print(" , ");
        //Serial.print(AcY);
        //Serial.print(" , ");
        //Serial.println(AcZ);
        delay(0.1);
      }
 
    client.stop();
    Serial.println("Client disconnected");
 
  }
}

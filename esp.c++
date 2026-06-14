#include <WiFi.h>

const char* ssid = "WIFI_NAME"; 
const char* password = "WIFI_PASSWORD";

WiFiServer server(8080);

void setup() {
  Serial.begin(115200);
  
  Serial.println("WiFi-connecting");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
 
  Serial.println("\n Connecyed!");
  Serial.print("ESP's IP Address: ");
  Serial.println(WiFi.localIP());
  
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        
        String data = client.readStringUntil('\n'); 
        
        int commaIndex = data.indexOf(',');
        
        if (commaIndex > 0) {
          String leftStr = data.substring(0, commaIndex);
          String rightStr = data.substring(commaIndex + 1);
          
          int pwm_l = leftStr.toInt();
          int pwm_r = rightStr.toInt();
          
          Serial.print("Left Wheel Speed: ");
          Serial.print(pwm_l);
          Serial.print(" | Right Wheel Speed: ");
          Serial.println(pwm_r);
          
        }
      }
    }
    client.stop();
  }
}

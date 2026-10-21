#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const char* mqttServer = "bemfa.com";
const int mqttPort = 9501;
const char* clientId = "YOUR_BEMFA_PRIVATE_KEY";
const char* topic = "esp32room"; 
#define DHTPIN 4          
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  dht.begin();
  delay(2000); 
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi已连接");

  client.setServer(mqttServer, mqttPort);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(clientId)) { 
      Serial.println("巴法云连接成功！🎉");
    } else {
      Serial.print("失败, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h) || t == 0 || h == 0) {
    Serial.println("传感器数据异常，跳过本次发送");
  } else {
    String payload = "Temp:" + String(t, 1) + ",Humi:" + String(h, 1);
    if(client.publish(topic, payload.c_str())) {
      Serial.println("发送成功: " + payload);
    }
  }
  delay(5000); 
}
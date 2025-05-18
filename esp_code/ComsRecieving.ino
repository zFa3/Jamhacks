#include <WiFi.h>

const char* ssid = "JamHacks";
const char* password = "jamhacks2025";

WiFiServer server(80);

void setup() {

  pinMode(2, OUTPUT);
  pinMode(17, OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected!");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Client connected");
    String data = "";
    while (client.connected()) {
      while (client.available()) {
        char c = client.read();
        data += c;
      }
      if (data.length() > 0) {
        Serial.print("Received: ");
        Serial.println(data);

        if (data == "ON") {
          digitalWrite(2, HIGH);
          digitalWrite(17, HIGH);
        } else if (data == "OFF") {
          digitalWrite(2, LOW);
          digitalWrite(17, LOW);
        }

        break;
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}

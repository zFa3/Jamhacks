// ESP32S Dev Module (Receiver)
// current ptg
#include <WiFi.h>

const char* ssid = "JamHacks";
const char* password = "jamhacks2025";

WiFiServer server(80);

void setup() {
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

        // Optionally respond
        // client.println("OK");

        // Example: toggle LED based on message
        // if (data == "ON") {
        //   digitalWrite(2, HIGH);
        // } else if (data == "OFF") {
        //   digitalWrite(2, LOW);
        // }

        break;
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}
//-------------------------------------------------------
// #include <WiFi.h>

// const char* ssid = "JamHacks";
// const char* password = "jamhacks2025";

// void setup() {
//   Serial.begin(115200);
//   WiFi.begin(ssid, password);

//   Serial.print("Connecting to WiFi");
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }

//   Serial.println("\nConnected to WiFi!");
//   Serial.print("ESP32 IP address: ");
//   Serial.println(WiFi.localIP());
// }

// void loop() {
//   // Nothing needed here to get the IP
// }
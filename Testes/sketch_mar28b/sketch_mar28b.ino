#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Revlo1";          // Replace with your network SSID
const char* password = "Torredeiluminacao1@";  // Replace with your network password
const char* mqtt_server = "34.59.67.57";  // Replace with your MQTT broker
const int mqtt_port = 1883;
const char* mqtt_username = "Revlo"; // Replace with your MQTT username
const char* mqtt_password = "Revlo123"; // Replace with your MQTT password

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  Serial.begin(115200);

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
     if (client.connect("ESP32Client", mqtt_username, mqtt_password)) { 
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 1000) {  // Send a message every second
    lastMsg = now;

   int randomNumber = random(0, 100);  // Generate random number between 0 and 100
    snprintf(msg, 50, "Random Number: %d", randomNumber);
    Serial.print("Publishing message: ");
    Serial.println(msg);
    MQTT.publish(TOPIC_PUBLISH, "1");//client.publish("esp32/random", msg);  // Publish message to topic "esp32/random"
  }
}
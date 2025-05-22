#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "shien";
const char* password = "123456789";

// FastAPI endpoint and token
const char* serverName = "https://backendappdev.onrender.com/temperature";
String bearerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0In0.WgCP_EgePnkULgyIdaUeyXf-K0U-hW7N5Q9__IoQsho";  // Replace with actual token

// DHT sensor
#define DHTPIN 14         // GPIO pin connected to DHT11
#define DHTTYPE DHT11    // DHT11 type
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    Serial.print("Sending Temperature: ");
    Serial.print(temperature);
    Serial.print("°C | Humidity: ");
    Serial.print(humidity);
    Serial.println("%");


    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
      delay(5000);
      return;
    }

    // Prepare JSON data
    String jsonData = "{\"temperature\": " + String(temperature, 1) +
                      ", \"humidity\": " + String(humidity, 1) + "}";

    // POST request
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer " + bearerToken);

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("HTTP ");
      Serial.print(httpResponseCode);
      Serial.print(" Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(3000); // wait 3 seconds before next send
}
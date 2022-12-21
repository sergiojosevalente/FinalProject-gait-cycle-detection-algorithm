#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <WiFi.h> // Enables the ESP32 to connect to the local network (via WiFi)
#include "PubSubClient.h" // Connect and publish to the MQTT broker

Adafruit_MPU6050 mpu;

// WiFi
const char *ssid = "Sergio"; // Enter your WiFi name
const char *wifi_password = "sergio123";  // Enter WiFi password

// MQTT ESP3 = Tangan Dada
const char* mqtt_server = "192.168.43.248";  // IP of the MQTT broker
const char* mpu5060_topic = "wban/sensor/esp3";
const char* mqtt_username = "sergiocorbymqtt"; // MQTT username
const char* mqtt_password = "SergioCorby"; // MQTT password
const char* clientID = "client_mpu5060"; // MQTT client ID

int y;
int i;

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient); 

void setup() {
  Serial.begin(115200);
  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);
// Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    y++;
    delay(500);
    Serial.print(".");
    Serial.print(y);
    if (y>=11) {
      ESP.restart();
      y = 0;
    }
  }
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens
  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);
}

// Custom function to connet to the MQTT broker via WiFi
void connect_MQTT(){
  Serial.print("Connecting to ");
  Serial.println(ssid);
  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  // If the connection is failing, make sure you are using the correct MQTT Username and Password (Setup Earlier in the Instructable)
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}

void loop() {

  connect_MQTT();
  Serial.setTimeout(2000);
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  Serial.print("Xesp3: ");
  Serial.print(a.acceleration.x);
  Serial.print("Rssiesp3: ");
  Serial.println(WiFi.RSSI());
  Serial.println("");
  delay(500);

  // MQTT can only transmit strings
// MQTT can only transmit strings
  String esp3= "Rssiesp3:"+String((float)WiFi.RSSI()) + " " "Axesp3:"+String((float)a.acceleration.x);

    // PUBLISH to the MQTT Broker (topic = mpu5060, defined at the beginning)

   if (client.publish(mpu5060_topic, esp3.c_str())) {
    Serial.println("esp3 sent!");
  }
  // Again, client.publish will return a boolean value depending on whether it succeded or not.
  // If the message failed to send, we will try again, as the connection may have broken.
  else {
    Serial.println("Axesp1 failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(mpu5060_topic, esp3.c_str());
  }
  client.disconnect();  // disconnect from the MQTT broker
  delay(0.20);       // print new values every 1 Minute
}

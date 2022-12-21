import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.43.248'
MQTT_USER = 'sergiocorbymqtt'
MQTT_PASSWORD = 'SergioCorby'
MQTT_TOPIC = 'wban/sensor/#'


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    item = str(msg.payload.decode("utf-8"))
    print(item)


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()


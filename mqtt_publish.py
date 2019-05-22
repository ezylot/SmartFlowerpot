import paho.mqtt.publish as publish
 
MQTT_SERVER = "192.168.43.136"
MQTT_PATH = "SmartFlowerpot"
 
publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)
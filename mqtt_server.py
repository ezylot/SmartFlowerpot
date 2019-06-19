import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep,time
 
MQTT_SERVER = "localhost"
MQTT_PATH = "SmartFlowerpot"
pin = 24

# set GPIO Mode 
GPIO.setmode(GPIO.BCM)
# setup GPIO pins
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, False)

lastchange = time()
dif = 5

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    global lastchange
    global dif
    lastchange = time()
    if float(msg.payload) > 26:
        dif = 2
    else:
        dif = 6
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
while True:
    if time() - lastchange > dif:
        GPIO.output(pin, True)
    else:
        print("no need to water the plants yet " + str(time() - lastchange))
        GPIO.output(pin,False)
    sleep(0.1)
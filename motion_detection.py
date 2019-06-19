#!/usr/bin/python

import picamera
import picamera.array
import subprocess
import time
import paho.mqtt.publish as publish
from sense_hat import SenseHat

 
MQTT_SERVER = "192.168.43.136"
MQTT_PATH = "SmartFlowerpot"

threshold = 10    # How Much pixel changes
sensitivity = 2000 # How many pixels change

sense = SenseHat()
sense.clear()

def takeMotionImage(width, height):
    with picamera.PiCamera() as camera:
        time.sleep(0.2)
        camera.resolution = (width, height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            return stream.array

def scanMotion(width, height):
    motionFound = False
    data1 = takeMotionImage(width, height)
    while not motionFound:
        data2 = takeMotionImage(width, height)
        diffCount = 0;
        for w in range(0, width):
            for h in range(0, height):
                # get the diff of the pixel. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
                if  diff > threshold:
                    diffCount += 1
            if diffCount > sensitivity:
                break;
        if diffCount > sensitivity:
            motionFound = True
        else:
            data2 = data1
    return motionFound

def motionDetection():
    print("Scanning for Motion threshold=%i sensitivity=%i..."  % (threshold, sensitivity))
    while True:
       # try:
          if scanMotion(224, 160):
              temp = sense.get_temperature()
              cpu_temp = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
              realtemp = temp - (((float(cpu_temp)/1000) - temp)/1.2)
              print ("Motion detected --> Temperatur is: " + str(realtemp))
              try:
                publish.single(MQTT_PATH, str(realtemp), hostname=MQTT_SERVER)
              except:
                print("server unreachable")
      #  except:
      #    print("something went wrong")

if __name__ == '__main__':
    try:
        motionDetection()
    finally:
        print("Exiting Program")

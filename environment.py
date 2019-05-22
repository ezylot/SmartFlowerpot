from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

round_digits = 2

while True:
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()

    temp = round(temp, round_digits)
    humidity = round(humidity, round_digits)
    pressure = round(pressure, round_digits)

    print("{},{:7.2f},{:7.2f},{:8.2f}".format(
        int(round(time.time() * 1000)), temp, humidity, pressure))

    time.sleep(0.5)
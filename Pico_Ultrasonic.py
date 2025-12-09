# simpan kode ini dengan nama main.py

from machine import Pin, time_pulse_us
import utime
# Ultrasonic pins
TRIG = Pin(19, Pin.OUT)
ECHO = Pin(20, Pin.IN)
def get_distance():
    TRIG.low()
    utime.sleep_us(5)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()
    duration = time_pulse_us(ECHO, 1, 30000)
    distance = (duration / 2) / 29.1
    return distance
while True:
    d = get_distance()
    # silahkan atur timer sesuai preferensi anda dengan syntax utime.sleep("nilai yg anda inginkan") 
    print(d)
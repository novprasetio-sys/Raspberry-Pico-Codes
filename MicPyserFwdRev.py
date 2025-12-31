# MicroPython Forward & Reverse Control via USB (sys.stdin.buffer)
# Raspberry Pi Pico
# LED Forward = Pin 14
# LED Reverse = Pin 15
# Integer commands: 1 = Forward, 2 = Reverse, 0 = Stop

import sys
from machine import Pin
import time

# Inisialisasi LED indikator
led_forward = Pin(14, Pin.OUT)
led_reverse = Pin(15, Pin.OUT)

# Fungsi untuk set arah
def set_forward():
    led_forward.value(1)   # Nyalakan LED Forward
    led_reverse.value(0)   # Matikan LED Reverse

def set_reverse():
    led_forward.value(0)   # Matikan LED Forward
    led_reverse.value(1)   # Nyalakan LED Reverse

def stop_all():
    led_forward.value(0)
    led_reverse.value(0)

# Loop utama, baca 1 byte dari USB
while True:
    data = sys.stdin.buffer.read(1)  # baca 1 byte integer
    if data:
        cmd = int.from_bytes(data, 'little')  # konversi ke integer
        if cmd == 1:
            set_forward()
        elif cmd == 2:
            set_reverse()
        elif cmd == 0:
            stop_all()
# OneWire.py

import machine

class OneWire:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.pin.value(1)

    def reset(self):
        self.pin.value(0)
        time.sleep_us(480)
        self.pin.value(1)
        time.sleep_us(70)
        return self.pin.value() == 0

    def write_byte(self, byte):
        for i in range(8):
            self.pin.value(0)
            time.sleep_us(10)
            self.pin.value((byte >> i) & 1)
            time.sleep_us(50)
            self.pin.value(1)
            time.sleep_us(10)

    def read_byte(self):
        byte = 0
        for i in range(8):
            self.pin.value(0)
            time.sleep_us(10)
            self.pin.value(1)
            time.sleep_us(10)
            byte |= self.pin.value() << i
            time.sleep_us(50)
        return byte
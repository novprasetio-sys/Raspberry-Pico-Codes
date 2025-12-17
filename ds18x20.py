# ds18x20.py

import onewire
import time

class DS18X20:
    def __init__(self, onewire):
        self.ow = onewire
        self.roms = []

    def scan(self):
        self.ow.reset()
        self.ow.write_byte(0xF0)
        rom = bytearray(8)
        for i in range(8):
            rom[i] = self.ow.read_byte()
        self.roms = [rom]
        return self.roms

    def convert_temp(self):
        self.ow.reset()
        self.ow.write_byte(0xCC)
        self.ow.write_byte(0x44)

    def read_temp(self, rom):
        self.ow.reset()
        self.ow.write_byte(0xCC)
        self.ow.write_byte(0xBE)
        data = bytearray(9)
        for i in range(9):
            data[i] = self.ow.read_byte()
        temp_lsb = data[0]
        temp_msb = data[1]
        temp = (temp_msb << 8 | temp_lsb) / 16
        return temp
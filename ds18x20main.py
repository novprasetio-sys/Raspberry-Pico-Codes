#main.py

import machine
import time
import onewire
import ds18x20

# Inisialisasi pin
ds_pin = machine.Pin(2)  # Pin untuk sensor DS18B20
relay_pin = machine.Pin(3, machine.Pin.OUT)  # Pin untuk relay
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

while True:
    try:
        # Baca data DS18B20
        roms = ds_sensor.scan()
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        temperature = ds_sensor.read_temp(roms[0])

        # Hidupkan pin jika temperatur >= 35°C
        if temperature >= 35:
            relay_pin.value(1)
        else:
            relay_pin.value(0)
    except Exception as e:
        print('Error:', e)
    time.sleep(1)
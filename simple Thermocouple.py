from machine import ADC, Pin
import time

# Output
led = Pin(25, Pin.OUT)
relay = Pin(2, Pin.OUT)

# Input ADC GP26 (ADC0)
adc = ADC(26)

while True:
    adc_value = adc.read_u16()               # 0 - 65535
    voltage = adc_value * 3.3 / 65535       # Konversi ke Volt
    
    # Simulasi LM35 (10mV per °C)
    tempt = voltage * 100                   # lebih simpel
    
    print("ADC:", adc_value,
          "Voltage:", round(voltage, 3), "V",
          "Suhu:", round(tempt, 2), "°C")

    if tempt >= 40:
        led.value(1)
        relay.value(1)
    else:
        led.value(0)
        relay.value(0)

    time.sleep(0.5)
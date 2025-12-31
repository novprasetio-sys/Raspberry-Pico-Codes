import machine
import time

button = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin('LED', machine.Pin.OUT)

led_state = 0          # 0 = OFF, 1 = ON
last_btn = 1           # default HIGH

while True:
    now_btn = button.value()

    # Detect button press (HIGH -> LOW)
    if last_btn == 1 and now_btn == 0:
        led_state = not led_state
        led.value(not led_state)   # active-low handling
        print("LED:", led_state)

    last_btn = now_btn
    time.sleep(0.02)   # debounce ringan
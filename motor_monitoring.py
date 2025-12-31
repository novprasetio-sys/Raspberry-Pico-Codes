import machine
import time

# Input pin pull-up
kincir1 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
kincir2 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

last_state1 = 1
last_state2 = 1

while True:
    state1 = kincir1.value()
    state2 = kincir2.value()
    
    # Kincir 1 gangguan (LOW = tombol ditekan)
    if last_state1 == 1 and state1 == 0:
        print("Kincir 1 bermasalah")
        
    # Kincir 2 gangguan
    if last_state2 == 1 and state2 == 0:
        print("Kincir 2 bermasalah")
    
    last_state1 = state1
    last_state2 = state2
    
    time.sleep(0.02)  # debounce ringan
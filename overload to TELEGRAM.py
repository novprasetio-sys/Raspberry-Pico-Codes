import network
import urequests
import time
from machine import Pin

SSID = "WIFI"
PASSWORD = "PASSWORD"

BOT_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

URL = "https://api.telegram.org/bot"+BOT_TOKEN+"/sendMessage"

overload = Pin(15, Pin.IN, Pin.PULL_UP)

last_state = overload.value()

# koneksi wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("WiFi Connected")

while True:

    state = overload.value()

    if state != last_state:

        if state == 0:
            msg = "⚠️ OVERLOAD TRIP"

        else:
            msg = "✅ OVERLOAD NORMAL"

        url = URL+"?chat_id="+CHAT_ID+"&text="+msg
        urequests.get(url)

        print(msg)

        last_state = state

    time.sleep(1)
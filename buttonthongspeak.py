import network
from machine import Pin
import urequests
import time

# ==========================
# KONFIGURASI WIFI & THINGSPEAK
# ==========================
SSID = "FEEDING"
PASSWORD = "autofeeding"
API_KEY = "xxxxxxxxxxxxx"
URL = "https://api.thingspeak.com/update"

BUTTON_PIN = 22

# ==========================
# KONEKSI WIFI
# ==========================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
print("Wi-Fi connected, IP:", wlan.ifconfig()[0])

# ==========================
# INISIALISASI PIN
# ==========================
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
last_state = -1

# ==========================
# LOOP UTAMA
# ==========================
while True:
    state = button.value()
    
    if state != last_state:
        last_state = state
        
        # Tentukan nilai yang akan dikirim
        send_value = 1 if state == 1 else 0
        
        # Tambahkan parameter unik agar entry baru selalu tercipta
        unique = int(time.time()*1000)  # timestamp ms untuk jamin entry baru
        
        try:
            url = f"{URL}?api_key={API_KEY}&field1={send_value}&status={unique}"
            response = urequests.get(url)
            entry_id = response.text.strip()
            print(f"Button state: {state} → send: {send_value}, entry_id: {entry_id}")
            response.close()
        except Exception as e:
            print("Error sending data:", e)
    
    time.sleep(15)  # debounce sederhana

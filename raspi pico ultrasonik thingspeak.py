import network
import urequests
import time
import machine

# ===== WiFi =====
SSID = "GUDANG A"
PASSWORD = "5c1.2024"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Menghubungkan WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("Terhubung ke WiFi:", wlan.ifconfig())

# ===== Ultrasonik HC-SR04 setup =====
TRIG_PIN = 19
ECHO_PIN = 20

trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

def baca_ultrasonik():
    try:
        trig.low()
        time.sleep_us(2)
        trig.high()
        time.sleep_us(10)
        trig.low()

        # Tunggu echo start
        timeout_start = time.ticks_us()
        while echo.value() == 0:
            if time.ticks_diff(time.ticks_us(), timeout_start) > 30000:  # 30 ms timeout
                raise Exception("No echo start")
        start = time.ticks_us()

        # Tunggu echo end
        timeout_start = time.ticks_us()
        while echo.value() == 1:
            if time.ticks_diff(time.ticks_us(), timeout_start) > 30000:  # 30 ms timeout
                raise Exception("No echo end")
        end = time.ticks_us()

        jarak = (time.ticks_diff(end, start)) / 58  # cm
        return round(jarak, 1)
    except Exception as e:
        print("Error Ultrasonik:", e)
        return None  # return None kalau error

# ===== Thingspeak =====
THINGSPEAK_API_KEY = "API_KEY_KAMU"  # ganti dengan API Key channel kamu
THINGSPEAK_URL = "http://api.thingspeak.com/update"

def kirim_thingspeak(jarak):
    if jarak is None:
        jarak = 0  # dummy value kalau sensor error
    url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={jarak}"
    try:
        response = urequests.get(url, timeout=10)
        print("Kirim ke Thingspeak:", jarak, "Status:", response.status_code)
        response.close()
    except Exception as e:
        print("Gagal kirim:", e)

# ===== Loop utama =====
while True:
    jarak = baca_ultrasonik()
    print("Jarak:", jarak, "cm")
    kirim_thingspeak(jarak)
    time.sleep(20)  # update tiap 20 detik
import network
import socket
import time
import dht
from machine import Pin

# ===== Inisialisasi DHT11 =====
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)  # ganti sesuai pin DATA DHT11
sensor = dht.DHT11(dht_pin)

# ===== Setup Access Point =====
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='PicoW_DHT11', password='12345678')
print("AP aktif!")
print("SSID: PicoW_DHT11")
print("Password: 12345678")
print("IP AP:", ap.ifconfig()[0])

time.sleep(2)  # tunggu AP siap

# ===== Fungsi HTML =====
def web_page(temp, hum):
    html = f"""
    <html>
    <head>
        <title>Monitoring Temperatur & Kelembaban</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; background: #e0f7fa; }}
            h1 {{ color: #006064; margin-top: 40px; }}
            p {{ font-size: 32px; color: #004d40; margin: 20px; }}
        </style>
    </head>
    <body>
        <h1>Monitoring temperatur & kelembaban</h1>
        <p>Suhu = {temp} °C</p>
        <p>Kelembaban = {hum} %</p>
    </body>
    </html>
    """
    return html

# ===== Setup Server =====
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Server siap! Sambungkan ke AP, buka browser di:", ap.ifconfig()[0])

# ===== Loop utama =====
while True:
    try:
        conn, addr = s.accept()
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        response = web_page(temperature, humidity)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print("Error:", e)
        time.sleep(2)
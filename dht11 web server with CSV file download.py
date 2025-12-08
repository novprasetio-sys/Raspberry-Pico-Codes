import network
import socket
import time
import dht
from machine import Pin
import os

# ===== Inisialisasi DHT11 =====
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)  # ganti sesuai pin DATA DHT11
sensor = dht.DHT11(dht_pin)

# ===== Setup Access Point =====
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='PicoW_DHT11', password='12345678')
print("AP aktif! SSID: PicoW_DHT11, Password: 12345678")
print("IP AP:", ap.ifconfig()[0])

time.sleep(2)  # tunggu AP siap

# ===== File CSV =====
CSV_FILE = "dht11_data.csv"
if CSV_FILE not in os.listdir():
    with open(CSV_FILE, "w") as f:
        f.write("Timestamp,Suhu_C,Kelembaban_%\n")

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
            .button {{
                display: inline-block;
                padding: 15px 25px;
                font-size: 20px;
                margin: 20px;
                cursor: pointer;
                background-color: #00838f;
                color: white;
                border: none;
                border-radius: 8px;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <h1>Monitoring Temperatur & Kelembaban</h1>
        <p>Suhu = {temp} °C</p>
        <p>Kelembaban = {hum} %</p>
        <a href="/download" class="button">Download CSV</a>
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
        request = conn.recv(1024)
        request = request.decode('utf-8')

        # Baca sensor
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Timestamp manual
        t = time.localtime()
        timestamp = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
            t[0], t[1], t[2], t[3], t[4], t[5]
        )

        # Simpan ke CSV
        with open(CSV_FILE, "a") as f:
            f.write(f"{timestamp},{temperature},{humidity}\n")

        # Cek route
        if "GET /download" in request:
            # Kirim file CSV
            try:
                with open(CSV_FILE, "r") as f:
                    conn.send('HTTP/1.1 200 OK\n')
                    conn.send('Content-Type: text/csv\n')
                    conn.send('Content-Disposition: attachment; filename="dht11_data.csv"\n')
                    conn.send('Connection: close\n\n')
                    for line in f:
                        conn.send(line)
            except:
                conn.send("HTTP/1.1 404 Not Found\n\nFile not found")
        else:
            # Kirim halaman web biasa
            response = web_page(temperature, humidity)
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)

        conn.close()
    except Exception as e:
        print("Error:", e)
        time.sleep(2)
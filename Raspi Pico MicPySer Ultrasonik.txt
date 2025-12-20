**Judul Artikel:**
Membuat Sistem Monitoring Jarak Interaktif dengan Micropython dan Python
**Konten Artikel:**
Pendahuluan
------------
Sistem monitoring jarak interaktif sangat penting dalam berbagai aplikasi, seperti pengawasan jarak antara objek, pengawasan jarak antara kendaraan, dan lain-lain. Dalam artikel ini, kita akan membuat sistem monitoring jarak interaktif menggunakan Micropython dan Python.
**Komponen yang Diperlukan:**
* 1x Pico 16 MB untuk Micropython)
* 1x Sensor Ultrasonik
* 1x Buzzer
* 1x Komputer (untuk MicPySer)
* 1x Kabel USB
**Kode Micropython:**
```
# Micropython code
from machine import Pin, time_pulse_us
import utime
import time
# Ultrasonic pins
TRIG = Pin(19, Pin.OUT)
ECHO = Pin(18, Pin.IN)
buzzer = Pin(25, Pin.OUT)
def get_distance():
    TRIG.low()
    utime.sleep_us(5)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()
    duration = time_pulse_us(ECHO, 1, 30000)
    distance = (duration / 2) / 29.1
    return distance
while True:
    d = get_distance()
    print(d)
    if d <= 5:
        buzzer.value(1)
    else:
        buzzer.value(0)
    time.sleep(0.1)
```
**Kode MicPySer (Python):**
```
# python code
import tkinter as tk
import serial
import time

Koneksi serial (ganti port sesuai)
ser = serial.Serial('COM3', 115200, timeout=1)

def update_gui():
    if ser.in_waiting > 0:
        jarak = ser.readline().decode('utf-8').strip()
        try:
            jarak = float(jarak)
            label_jarak.config(text=f"Jarak: {jarak:.1f} cm")
            if jarak <= 5:
                label_notif.config(text="⚠️ Jarak Terlalu Dekat!", fg="red")
                canvas.create_oval(10, 10, 100, 100, fill="red")
            else:
                label_notif.config(text="✅ Aman", fg="green")
                canvas.create_oval(10, 10, 100, 100, fill="green")
        except:
            pass
    root.after(100, update_gui)

root = tk.Tk()
root.title("Monitor Jarak Interaktif")

Label Jarak
label_jarak = tk.Label(root, text="Jarak: -- cm", font=("Arial", 30))
label_jarak.pack(pady=20)

Notifikasi
label_notif = tk.Label(root, text="", font=("Arial", 18))
label_notif.pack(pady=10)

Indikator LED
canvas = tk.Canvas(root, width=110, height=110)
canvas.pack(pady=10)

Tombol Koneksi
btn_reconnect = tk.Button(root, text="Reconnect", command=lambda: ser.open() if not ser.is_open else print("Sudah konek"))
btn_reconnect.pack(pady=10)

update_gui()
root.mainloop()
```
**Cara Kerja Sistem:**
1. Sensor ultrasonik mendeteksi jarak antara objek dan mengirimkan data ke Pico.
2. Pico menerima data jarak dan mengirimkannya ke komputer melalui serial.
3. Python menerima data jarak dari serial dan menampilkannya di GUI.
4. Jika jarak <= 5 cm, maka buzzer akan berbunyi dan GUI akan menampilkan notifikasi "Jarak Terlalu Dekat!".
5. Jika jarak > 5 cm, maka buzzer akan diam dan GUI akan menampilkan notifikasi "Aman".

**Kesimpulan:**
Dalam artikel ini, kita telah membuat sistem monitoring jarak interaktif menggunakan Micropython dan Python. Sistem ini dapat mendeteksi jarak antara objek dan menampilkannya di GUI, serta memberikan notifikasi jika jarak terlalu dekat.
Silakan Anda edit dan tambahkan konten sesuai kebutuhan Anda!
Saya harap artikel ini membantu!
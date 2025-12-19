# MicPySer Interaktif: Monitor Jarak dengan Pico & Python GUI

Proyek ini menggunakan Raspberry Pi Pico (MicroPython) untuk membaca sensor ultrasonik HC-SR04 dan mengirim data jarak ke PC. GUI Python (Tkinter) menampilkan jarak realtime dengan indikator LED dan notifikasi interaktif.

## Fitur
- Baca jarak HC-SR04 via Pico
- GUI interaktif di PC (Tkinter)
- Indikator LED (hijau/merah)
- Notifikasi "Jarak Terlalu Dekat!" jika <= 5 cm
- Tombol Reconnect serial

## Struktur Proyek
- `pico_code.py`: Kode MicroPython untuk Pico
- `gui_interaktif.py`: Kode Python GUI di PC
- `README.md`: Dokumentasi proyek

## Cara Pakai
1. Upload `pico_code.py` ke Pico.
2. Sambungkan HC-SR04 dan buzzer ke Pico.
3. Jalankan `gui_interaktif.py` di PC.
4. Lihat jarak realtime dan notifikasi di GUI.

## Koneksi
- Pico -> PC via USB (Serial)
- Sensor HC-SR04 -> Pico (pin 2=echo, 3=trigger)
- Buzzer -> Pico (pin 4)

## Dependensi
- MicroPython (Pico)
- Python 3 + Tkinter + pyserial (PC)

## Screenshot GUI
![GUI Interaktif](screenshot_gui.png) (tambah screenshot jika perlu)

## main.py

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


## GUI.py


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


## Author
Novan Prasetio (MicPySer Project)


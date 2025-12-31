# GUI Python Forward & Reverse Control via USB
# Mengirim 1 byte integer ke Raspberry Pi Pico
# 1 = Forward, 2 = Reverse, 0 = Stop

import serial
import time
import tkinter as tk

# Sesuaikan COM port Pico kamu
ser = serial.Serial('COM8', 115200, timeout=1)
time.sleep(2)  # Tunggu Pico siap

# Fungsi kirim command integer
def send_cmd(value):
    if ser.is_open:
        ser.write(bytes([value]))  # kirim 1 byte
        ser.flush()
        time.sleep(0.05)           # delay kecil biar Pico sempat baca

# Fungsi tombol GUI
def forward():
    send_cmd(1)
    status_label.config(text="Status: Forward")

def reverse():
    send_cmd(2)
    status_label.config(text="Status: Reverse")

def stop():
    send_cmd(0)
    status_label.config(text="Status: Stop")

# Setup GUI Tkinter
root = tk.Tk()
root.title("Forward & Reverse Control")

tk.Button(root, text="Forward", width=15, command=forward).pack(pady=5)
tk.Button(root, text="Reverse", width=15, command=reverse).pack(pady=5)
tk.Button(root, text="Stop", width=15, command=stop).pack(pady=5)

status_label = tk.Label(root, text="Status: Stop", fg="blue")
status_label.pack(pady=10)

root.mainloop()
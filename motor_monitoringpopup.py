import serial
import threading
import tkinter as tk
from tkinter import messagebox

# Ganti COM port sesuai Pico W
ser = serial.Serial('COM5', 115200, timeout=0.1)

def read_serial():
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            if "Kincir 1 bermasalah" in line:
                root.after(0, lambda: messagebox.showwarning("Alert", "Kincir 1 Bermasalah!"))
            elif "Kincir 2 bermasalah" in line:
                root.after(0, lambda: messagebox.showwarning("Alert", "Kincir 2 Bermasalah!"))

# GUI dasar
root = tk.Tk()
root.title("Monitoring Kincir")
root.geometry("300x100")

label = tk.Label(root, text="Monitoring Kincir...", font=("Arial", 14))
label.pack(pady=20)

# Thread serial
threading.Thread(target=read_serial, daemon=True).start()

root.mainloop()
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

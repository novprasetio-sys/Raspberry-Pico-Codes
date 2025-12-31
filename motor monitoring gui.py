import serial
import threading
import tkinter as tk

# Ganti COM port sesuai Pico W
# Kalau mau test dulu tanpa Pico, bisa set ser = None
try:
    ser = serial.Serial('COM5', 115200, timeout=0.1)
except:
    ser = None

root = tk.Tk()
root.title("Monitoring Kincir")
root.geometry("350x250")

# Status Kincir 1
frame1 = tk.Frame(root, width=300, height=50, bg='green')
frame1.pack(pady=10)
label1 = tk.Label(frame1, text="Kincir 1: Normal", font=("Arial", 12), bg='green', fg='white')
label1.pack()
btn_reset1 = tk.Button(frame1, text="Reset Kincir 1", command=lambda: update_status(1, True))
btn_reset1.pack(pady=5)

# Status Kincir 2
frame2 = tk.Frame(root, width=300, height=50, bg='green')
frame2.pack(pady=10)
label2 = tk.Label(frame2, text="Kincir 2: Normal", font=("Arial", 12), bg='green', fg='white')
label2.pack()
btn_reset2 = tk.Button(frame2, text="Reset Kincir 2", command=lambda: update_status(2, True))
btn_reset2.pack(pady=5)

def update_status(kincir, normal):
    if kincir == 1:
        if normal:
            frame1.config(bg='green')
            label1.config(text="Kincir 1: Normal", bg='green')
        else:
            frame1.config(bg='red')
            label1.config(text="Kincir 1: Bermasalah", bg='red')
    elif kincir == 2:
        if normal:
            frame2.config(bg='green')
            label2.config(text="Kincir 2: Normal", bg='green')
        else:
            frame2.config(bg='red')
            label2.config(text="Kincir 2: Bermasalah", bg='red')

def read_serial():
    if not ser:
        return
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            if "Kincir 1 bermasalah" in line:
                root.after(0, lambda: update_status(1, False))
            elif "Kincir 2 bermasalah" in line:
                root.after(0, lambda: update_status(2, False))

# Thread serial
threading.Thread(target=read_serial, daemon=True).start()

# ==== Simulasi gangguan untuk testing tanpa Pico ====
def simulate_kincir1():
    update_status(1, False)
def simulate_kincir2():
    update_status(2, False)

sim_frame = tk.Frame(root)
sim_frame.pack(pady=10)
tk.Button(sim_frame, text="Simulasi Kincir 1 Gangguan", command=simulate_kincir1).pack(side='left', padx=5)
tk.Button(sim_frame, text="Simulasi Kincir 2 Gangguan", command=simulate_kincir2).pack(side='left', padx=5)

root.mainloop()
#buat kode in di Python dan hubungkan pico ke laptop/PC secara serial
import tkinter as tk
import serial
import csv
from datetime import datetime

# Koneksi serial (MicPySer)
try:
    ser = serial.Serial('COM3', 115200, timeout=1)
except:
    print("Gagal menyambung ke COM3. Pastikan Pico sudah terhubung.")

# Variabel untuk Logging
data_log = []
is_logging = False

def toggle_logging():
    global is_logging
    if not is_logging:
        is_logging = True
        btn_csv.config(text="Berhenti & Simpan CSV", bg="#ff6666")
    else:
        is_logging = False
        save_to_file()
        btn_csv.config(text="Mulai Simpan CSV", bg="#66ff66")

def save_to_file():
    if data_log:
        # Nama file otomatis berdasarkan waktu saat ini
        filename = datetime.now().strftime("Log_MicPySer_%Y%m%d_%H%M%S.csv")
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Jarak (cm)']) # Header CSV
            writer.writerows(data_log)
        print(f"Data tersimpan di {filename}")
        data_log.clear() # Kosongkan list setelah disimpan

def update_gui():
    global is_logging
    if ser.in_waiting > 0:
        raw_data = ser.readline().decode('utf-8').strip()
        try:
            jarak = float(raw_data)
            label_jarak.config(text=f"Jarak: {jarak:.1f} cm")
            
            # Logika Notifikasi
            if jarak <= 5:
                label_notif.config(text="⚠️ Jarak Terlalu Dekat!", fg="red")
            else:
                label_notif.config(text="✅ Aman", fg="green")
            
            # Jika tombol log aktif, simpan data ke list RAM
            if is_logging:
                timestamp = datetime.now().strftime("%H:%M:%S")
                data_log.append([timestamp, jarak])
                
        except ValueError:
            pass # Abaikan data korup
            
    root.after(100, update_gui)

# --- UI Setup ---
root = tk.Tk()
root.title("Monitor Jarak MicPySer")
root.geometry("400x350")

label_jarak = tk.Label(root, text="Jarak: -- cm", font=("Arial", 24, "bold"))
label_jarak.pack(pady=20)

label_notif = tk.Label(root, text="Menunggu data...", font=("Arial", 16))
label_notif.pack(pady=10)

# Tombol untuk CSV
btn_csv = tk.Button(root, text="Mulai Simpan CSV", font=("Arial", 12), 
                    command=toggle_logging, bg="#66ff66", width=20, height=2)
btn_csv.pack(pady=30)

update_gui()
root.mainloop()

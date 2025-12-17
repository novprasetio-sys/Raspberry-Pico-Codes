# Simple Temperature Controller (MicroPython)

Proyek ini adalah sistem kontrol suhu berbasis **MicroPython** yang menggunakan sensor suhu **DS18B20** dan **Relay Module**. Sistem akan secara otomatis mengaktifkan relay jika suhu mencapai ambang batas yang ditentukan ($T \ge 35^\circ C$).

## 🚀 Fitur Utama
* **Real-time Monitoring:** Membaca suhu melalui protokol OneWire.
* **Automated Control:** Logika switching relay berdasarkan setpoint suhu.
* **Error Handling:** Dilengkapi dengan blok `try-except` untuk menjaga stabilitas sistem dari kegagalan pembacaan sensor.

## 🛠️ Persyaratan Perangkat Terkait
* **Microcontroller:** Kompatibel dengan Raspberry Pi Pico, ESP32, atau ESP8266 (MicroPython Firmware).
* **Sensor:** DS18B20 (Waterproof atau Transistor-style).
* **Aktuator:** Relay Module (Active High).

## 🔌 Skema Koneksi
| Komponen | Pin Microcontroller | Fungsi |
|---|---|---|
| DS18B20 (Data) | GP2 / Pin 2 | OneWire Bus |
| Relay (IN) | GP3 / Pin 3 | Digital Output Control |
| VCC/GND | 3.3V / GND | Power Supply |

> **Catatan:** Jangan lupa tambahkan resistor *pull-up* $4.7k\Omega$ antara Pin Data DS18B20 dan VCC.

## 💻 Cara Penggunaan
1. Pastikan library `onewire` dan `ds18x20` sudah tersedia di dalam firmware MicroPython Anda (standar tersedia di sebagian besar build).
2. Unggah file `main.py` ke mikrokontroler Anda.
3. Sistem akan mulai melakukan *scanning* sensor dan mengontrol relay setiap detik.

## 📝 Logika Program
Program bekerja dengan alur sebagai berikut:
1. Melakukan inisialisasi pin dan protokol OneWire.
2. Memindai alamat ROM sensor DS18B20.
3. Mengonversi sinyal analog sensor ke data digital (suhu).
4. Melakukan komparasi: 
   - Jika **Suhu $\ge$ 35°C**, Pin 3 bernilai `HIGH` (Relay ON).
   - Jika **Suhu < 35°C**, Pin 3 bernilai `LOW` (Relay OFF).

## OneWire.py

import machine

class OneWire:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.pin.value(1)

    def reset(self):
        self.pin.value(0)
        time.sleep_us(480)
        self.pin.value(1)
        time.sleep_us(70)
        return self.pin.value() == 0

    def write_byte(self, byte):
        for i in range(8):
            self.pin.value(0)
            time.sleep_us(10)
            self.pin.value((byte >> i) & 1)
            time.sleep_us(50)
            self.pin.value(1)
            time.sleep_us(10)

    def read_byte(self):
        byte = 0
        for i in range(8):
            self.pin.value(0)
            time.sleep_us(10)
            self.pin.value(1)
            time.sleep_us(10)
            byte |= self.pin.value() << i
            time.sleep_us(50)
        return byte

---
Developed by **Novan Prasetio** | *Power Electronics & Microcontroller Enthusiast*

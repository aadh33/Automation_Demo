import tkinter as tk
import threading
import time
import pyfirmata2

# === Serial port for your Arduino ===
PORT = "COM22"   # Update to your port, e.g. "/dev/ttyUSB0" on Linux

# Setup board
board = pyfirmata2.Arduino(PORT)
it = pyfirmata2.util.Iterator(board)
it.start()

LED_PIN = 13
led = board.digital[LED_PIN]

# To track blinking state and avoid conflicts
blinking = False

# === LED Command Functions ===
def led_on():
    global blinking
    blinking = False
    led.write(1)

def led_off():
    global blinking
    blinking = False
    led.write(0)

def led_5_on_10_off():
    def task():
        global blinking
        blinking = True
        while blinking:
            led.write(1)
            time.sleep(5)
            if not blinking:
                break
            led.write(0)
            time.sleep(10)
    stop_blink()
    threading.Thread(target=task, daemon=True).start()

def blink_led():
    def task():
        global blinking
        blinking = True
        while blinking:
            led.write(1)
            time.sleep(0.5)
            if not blinking:
                break
            led.write(0)
            time.sleep(0.5)
    stop_blink()
    threading.Thread(target=task, daemon=True).start()

def led_5_on_only():
    stop_blink()
    def task():
        led.write(1)
        time.sleep(5)
        led.write(0)
    threading.Thread(target=task, daemon=True).start()

def led_10_off_only():
    stop_blink()
    led.write(0)
    def task():
        time.sleep(10)
    threading.Thread(target=task, daemon=True).start()

def stop_blink():
    global blinking
    blinking = False
    time.sleep(0.01) # Allow any running thread to break

def on_close():
    stop_blink()
    board.exit()
    root.destroy()

# === GUI Setup ===
root = tk.Tk()
root.title("Arduino LED Control")

tk.Button(root, text="Turn ON", width=20, command=led_on).pack(pady=5)
tk.Button(root, text="Turn OFF", width=20, command=led_off).pack(pady=5)
tk.Button(root, text="5s ON, 10s OFF (Loop)", width=20, command=led_5_on_10_off).pack(pady=5)
tk.Button(root, text="Blink (0.5s ON/OFF)", width=20, command=blink_led).pack(pady=5)
tk.Button(root, text="5 Seconds ON only", width=20, command=led_5_on_only).pack(pady=5)
tk.Button(root, text="10 Seconds OFF only", width=20, command=led_10_off_only).pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

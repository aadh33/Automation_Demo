import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import pyfirmata2
from datetime import datetime

# Serial port for your Arduino
PORT = "COM22"   # CHANGE THIS to your port, e.g. "/dev/ttyUSB0" for Linux

# Arduino board setup
board = pyfirmata2.Arduino(PORT)
it = pyfirmata2.util.Iterator(board)
it.start()
LED_PIN = 13
led = board.digital[LED_PIN]

# Logging
TEXT_LOG = "led_log.txt"
HTML_LOG = "led_log.html"

def log_action(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {action}"
    # Text log
    with open(TEXT_LOG, "a") as f:
        f.write(msg + "\n")
    # HTML log
    html_msg = f"<tr><td>{timestamp}</td><td>{action}</td></tr>\n"
    try:
        with open(HTML_LOG, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""
    if "<table" not in content:
        with open(HTML_LOG, "w") as f:
            f.write("<html><head><title>LED Action Log</title></head><body>\n")
            f.write("<h2>LED Action Log</h2>\n")
            f.write("<table border='1'><tr><th>Timestamp</th><th>Action</th></tr>\n")
            f.write(html_msg)
            f.write("</table></body></html>")
    else:
        new_content = content.replace("</table>", html_msg + "</table>")
        with open(HTML_LOG, "w") as f:
            f.write(new_content)

# Thread management
action_thread = None
stop_event = threading.Event()

def start_new_action(target):
    global action_thread, stop_event
    stop_current_action()
    stop_event = threading.Event()
    action_thread = threading.Thread(target=target, daemon=True)
    action_thread.start()

def stop_current_action():
    global stop_event, action_thread
    if stop_event:
        stop_event.set()
    if action_thread and action_thread.is_alive():
        action_thread.join(timeout=0.1)

# -- UI Commands
def led_on():
    def action():
        led.write(1)
        log_action('LED turned ON')
    start_new_action(action)

def led_off():
    def action():
        led.write(0)
        log_action('LED turned OFF')
    start_new_action(action)

def led_5_on_10_off():
    def action():
        log_action('Started 5s ON, 10s OFF loop')
        while not stop_event.is_set():
            led.write(1)
            log_action('LED ON (5s in ON/OFF loop)')
            for _ in range(50):
                if stop_event.is_set(): return
                time.sleep(0.1)
            led.write(0)
            log_action('LED OFF (10s in ON/OFF loop)')
            for _ in range(100):
                if stop_event.is_set(): return
                time.sleep(0.1)
    start_new_action(action)

def blink_led():
    def action():
        log_action("Started blinking (0.5s ON/OFF)")
        while not stop_event.is_set():
            led.write(1)
            log_action("LED BLINK ON (0.5s)")
            for _ in range(5):
                if stop_event.is_set(): return
                time.sleep(0.1)
            led.write(0)
            log_action("LED BLINK OFF (0.5s)")
            for _ in range(5):
                if stop_event.is_set(): return
                time.sleep(0.1)
    start_new_action(action)

def led_5_on_only():
    def action():
        led.write(1)
        log_action("LED ON for 5 seconds")
        for _ in range(50):
            if stop_event.is_set(): return
            time.sleep(0.1)
        led.write(0)
        log_action("LED OFF after 5 seconds")
    start_new_action(action)

def led_10_off_only():
    def action():
        led.write(0)
        log_action("LED OFF for 10 seconds")
        for _ in range(100):
            if stop_event.is_set(): return
            time.sleep(0.1)
        log_action("LED OFF 10 seconds complete")
    start_new_action(action)

# -- User-controlled ON for N seconds with validation and logging
def led_on_user_time():
    try:
        seconds_str = entry_seconds.get()
        seconds = float(seconds_str)
        if seconds < 0.1 or seconds > 3600:
            raise ValueError("Seconds must be between 0.1 and 3600")
        valid = True
    except Exception as e:
        valid = False
        error_msg = f"Validation failed for input '{entry_seconds.get()}': {e}"
        log_action(error_msg)
        messagebox.showerror("Invalid", "Please enter a valid number of seconds (0.1 to 3600).")
        return

def led_on_user_time():
    def action():
        try:
            seconds_str = entry_seconds.get()
            seconds = float(seconds_str)
            if seconds < 0.1 or seconds > 3600:
                raise ValueError("Seconds must be between 0.1 and 3600")
        except Exception as e:
            log_action(f"Validation failed for input '{entry_seconds.get()}': {e}")
            messagebox.showerror("Invalid", "Please enter a valid number of seconds (0.1 to 3600).")
            return

        led.write(1)
        log_action(f"LED ON for user-defined {seconds} seconds")
        on_seconds = 0
        # Count whole seconds
        for i in range(int(seconds)):
            if stop_event.is_set():
                led.write(0)
                log_action("LED OFF (user stopped action early)")
                return
            time.sleep(1)
            on_seconds += 1
        # Handle fractional second remainder
        leftover = seconds - int(seconds)
        if leftover > 0:
            if not stop_event.is_set():
                time.sleep(leftover)
                on_seconds += leftover
        led.write(0)
        log_action(f"LED OFF after user-defined {seconds} seconds")
        # Validation: allow for tiny timing errors
        if abs(on_seconds - seconds) < 0.05:
            log_action(f"Validation passed: LED ON duration matched {seconds} seconds")
        else:
            log_action(f"Validation failed: requested {seconds}s, but ON for {on_seconds:.2f}s")

    start_new_action(action)


def on_close():
    stop_current_action()
    board.exit()
    root.destroy()


# -- UI
root = tk.Tk()
root.title("Arduino LED Control")

frame = tk.Frame(root)
frame.pack(pady=5)
tk.Label(frame, text="Seconds ON:").grid(row=0, column=0, padx=4)
entry_seconds = tk.Entry(frame, width=8)
entry_seconds.grid(row=0, column=1, padx=4)
tk.Button(frame, text="LED ON (user seconds)", command=led_on_user_time, width=18).grid(row=0, column=2, padx=4)

tk.Button(root, text="Turn ON", width=25, command=led_on).pack(pady=5)
tk.Button(root, text="Turn OFF", width=25, command=led_off).pack(pady=5)
tk.Button(root, text="5s ON, 10s OFF (Loop)", width=25, command=led_5_on_10_off).pack(pady=5)
tk.Button(root, text="Blink (0.5s ON/OFF)", width=25, command=blink_led).pack(pady=5)
tk.Button(root, text="5 Seconds ON only", width=25, command=led_5_on_only).pack(pady=5)
tk.Button(root, text="10 Seconds OFF only", width=25, command=led_10_off_only).pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

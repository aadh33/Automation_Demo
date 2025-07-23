import re
import serial
import serial.tools.list_ports
import threading
import time
import os
from datetime import datetime

TEXT_LOG_FILE = "serial_log.txt"
HTML_LOG_FILE = "serial_log.html"

def ensure_html_log_initialized():
    """Initialize HTML log with header if not present."""
    if not os.path.exists(HTML_LOG_FILE):
        with open(HTML_LOG_FILE, "w") as f:
            f.write("<html><head><title>Serial Log</title></head><body>")
            f.write("<h2>Serial Communication Log</h2><hr>\n")

def log_message_plain(message):
    """Log message to plain text file with timestamp."""
    with open(TEXT_LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def log_message_html(tag, message):
    """Log message to HTML log with timestamp and tag (sent/received)."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = "#227722" if tag == "received" else "#2222aa"
    with open(HTML_LOG_FILE, "a") as f:
        f.write(
            f'<p><span style="color:gray">[{timestamp}]</span> '
            f'<span style="color:{color};"><strong>{tag.capitalize()}:</strong> {message}</span></p>\n'
        )

def close_html_log():
    """Close the HTML log properly at the end."""
    with open(HTML_LOG_FILE, "a") as f:
        f.write("<hr><p>Session ended.</p></body></html>\n")

def list_serial_devices():
    """Detect connected USB serial devices."""
    valid_ports = []
    all_ports = serial.tools.list_ports.comports()

    for i, port in enumerate(all_ports):
        if re.search(r'serial', port.description, re.IGNORECASE):
            valid_ports.append((i, port.device, port.description))

    return valid_ports

def select_serial_port():
    """Prompt user to select from available serial ports."""
    devices = list_serial_devices()

    if not devices:
        print("No USB Serial devices found.")
        return None

    print("Available USB Serial Devices:")
    for idx, device, desc in devices:
        print(f"[{idx}] {device} - {desc}")

    while True:
        try:
            choice = int(input("Select a device by its number: "))
            selected = next((d for d in devices if d[0] == choice), None)
            if selected:
                print(f"Selected device: {selected[1]} - {selected[2]}")
                return selected[1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def open_serial_connection(port, baudrate=9600, timeout=2):
    """Open and return a serial connection."""
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        print(f"Connected to {port} at {baudrate} baud.\n")
        return ser
    except serial.SerialException as e:
        print(f"Could not open serial port {port}: {e}")
        return None

def read_from_serial(serial_conn):
    """Continuously read from the serial port."""
    try:
        while True:
            if serial_conn.in_waiting > 0:
                response = serial_conn.readline().decode(errors="ignore").strip()
                if response:
                    print("Received:", response)
                    log_message_plain("Received: " + response)
                    log_message_html("received", response)
    except serial.SerialException:
        print("Serial connection lost.")
    except Exception as e:
        print(f"Error reading from serial: {e}")

def send_messages(serial_conn):
    """Continuously get user input and send to serial port."""
    try:
        while True:
            message = input("Enter Data (type 'exit' to quit): ").strip()
            if message.lower() == 'exit':
                break

            if not message.endswith('\n'):
                message += '\n'

            serial_conn.write(message.encode())
            print("Sent:", message.strip())
            log_message_plain("Sent: " + message.strip())
            log_message_html("sent", message.strip())

    except serial.SerialException:
        print("Serial connection lost while sending.")
    except Exception as e:
        print(f"Error sending to serial: {e}")

def main():
    print("Serial Communication Interface")
    print("-" * 40)

    baudrate = 9600
    timeout = 2

    ensure_html_log_initialized()

    port = select_serial_port()
    if not port:
        return

    serial_conn = open_serial_connection(port, baudrate=baudrate, timeout=timeout)
    if not serial_conn:
        return

    reader_thread = threading.Thread(target=read_from_serial, args=(serial_conn,), daemon=True)
    reader_thread.start()

    send_messages(serial_conn)

    serial_conn.close()
    close_html_log()
    print("Serial port closed. Logs saved to serial_log.txt and serial_log.html")

if __name__ == "__main__":
    main()

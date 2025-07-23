import serial
import time
import re

SERIAL_PORT = 'COM22'
BAUD_RATE = 57600
TIMEOUT = 15

def read_serial(port, baud):
    try:
        with serial.Serial(port, baud, timeout=1) as ser:
            time.sleep(2)
            print(f"Listening on {port}...")
            start = time.time()
            while time.time() - start < TIMEOUT:
                while ser.in_waiting:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    print(f"Received: '{line}'")
                    ascii_codes = [ord(c) for c in line]
                    print(f"ASCII: {ascii_codes}")
                    # Remove non-printables for better matching
                    clean = re.sub(r'[^\x20-\x7E]', '', line)
                    print(f"Cleaned: '{clean}'")
                    if "firmata.ino" in clean.lower():
                        print("Booted successfully")
                        return
            print("Timeout: 'firmata.ino' not received.")
    except Exception as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    read_serial(SERIAL_PORT, BAUD_RATE)

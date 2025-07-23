import serial
import time

# ---- Update this with your Arduino serial port ----
arduino_port = 'COM22'    # e.g., 'COM3' on Windows, '/dev/ttyACM0' on Linux
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for Arduino to reset and print its version

# Optional: Print all startup output from Arduino
while ser.in_waiting:
    print(ser.readline().decode().strip())

def send_command(cmd):
    ser.write((cmd+'\n').encode())  # Send the command with newline
    # Read response(s)
    time.sleep(0.1)
    while ser.in_waiting:
        print("Arduino:", ser.readline().decode().strip())

try:
    while True:
        user_cmd = input("Send 'ON' or 'OFF' to Arduino (or 'exit'): ").strip()
        if user_cmd.lower() == 'exit':
            break
        send_command(user_cmd)
except KeyboardInterrupt:
    pass
finally:
    ser.close()

import serial
import tkinter as tk

# Configure these parameters
SERIAL_PORT = 'COM23'      # Replace with your Arduino's port (e.g., 'COM3' on Windows or '/dev/ttyACM0' on Linux)
BAUD_RATE = 9600

# Establish the serial connection
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")

def led_on():
    arduino.write(b'1')

def led_off():
    arduino.write(b'0')

def blink_once():
    arduino.write(b'b')

root = tk.Tk()
root.title('Arduino LED Controller')

on_btn = tk.Button(root, text='Turn On', width=20, command=led_on)
on_btn.pack(pady=10)

off_btn = tk.Button(root, text='Turn Off', width=20, command=led_off)
off_btn.pack(pady=10)

blink_btn = tk.Button(root, text='Blink Once', width=20, command=blink_once)
blink_btn.pack(pady=10)

root.mainloop()

# Don't forget to close the serial connection when finished
arduino.close()

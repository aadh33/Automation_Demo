import pyfirmata2
import time

# Set the serial port name. Change this if your port is different.
PORT = "COM22"   # Example for Windows. Use "/dev/ttyUSB0" for Linux.

# Initialize the board connection
board = pyfirmata2.Arduino(PORT)

# Start the iterator thread to avoid buffer overflow
it = pyfirmata2.util.Iterator(board)
it.start()

LED_PIN = 13  # The built-in LED on Arduino Uno

print("Blinking LED on pin 13. Press Ctrl+C to exit.")

try:
    while True:
        board.digital[LED_PIN].write(1)  # LED ON
        time.sleep(0.5)
        board.digital[LED_PIN].write(0)  # LED OFF
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting and closing board connection.")
    board.exit()

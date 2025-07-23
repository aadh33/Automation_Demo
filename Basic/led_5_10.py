import pyfirmata2
import time

# Set the serial port name. Change this if your port is different.
PORT = "COM22"   # Example for Windows. Use "/dev/ttyUSB0" for Linux.

# Initialize the board connection
board = pyfirmata2.Arduino(PORT)

# Start the iterator thread to avoid buffer overflow
it = pyfirmata2.util.Iterator(board)
it.start()

LED_PIN = 13  # Built-in LED on Arduino Uno

print("Blinking LED: ON for 5 seconds, OFF for 10 seconds. Press Ctrl+C to exit.")

try:
    while True:
        board.digital[LED_PIN].write(1)  # LED ON
        time.sleep(5)                    # Wait for 5 seconds
        board.digital[LED_PIN].write(0)  # LED OFF
        time.sleep(10)                   # Wait for 10 seconds
except KeyboardInterrupt:
    print("Exiting and closing board connection.")
    board.exit()

import pyfirmata2
import time

try:
    board = pyfirmata2.Arduino('COM22')
    print("Board connected successfully!")

    it = pyfirmata2.util.Iterator(board)
    it.start()
    time.sleep(1)  # Let board settle

    LED_PIN = 13
    togglecount = 5

    for x in range(int(togglecount)):
        board.digital[LED_PIN].write(1)
        print(f"LED ON for iteration {x + 1}")
        time.sleep(1)
        board.digital[LED_PIN].write(0)
        print(f"LED OFF for iteration {x + 1}")
        time.sleep(1)

finally:
    board.exit()
    print("Board connection closed.")

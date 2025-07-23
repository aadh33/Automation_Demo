import serial
import serial.tools.list_ports
import time
import logging

LOG_FILENAME = 'arduino_test.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler()
    ]
)

ARDUINO_ID_HINTS = ['arduino', 'ch340', 'usb serial']  # Expand as needed

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        desc = port.description.lower()
        if any(hint in desc for hint in ARDUINO_ID_HINTS):
            return port.device
    return None

def send_and_log(ser, cmd, expected=None):
    logging.info(f"Sending: {cmd}")
    ser.write((cmd + '\n').encode())
    time.sleep(0.3)
    responses = []
    while ser.in_waiting:
        response = ser.readline().decode(errors='ignore').strip()
        responses.append(response)
        logging.info(f"Arduino: {response}")

    if expected:
        passed = any(expected in resp for resp in responses)
        if passed:
            logging.info(f"Test PASSED for '{cmd}': found expected '{expected}'")
        else:
            logging.warning(f"Test FAILED for '{cmd}': expected '{expected}' not found in responses: {responses}")
        return passed
    return True

def automated_test(ser):
    logging.info("[Auto Test] Starting ON/OFF test (failures allowed, tests independent)")

    # Test ON command
    try:
        send_and_log(ser, "ON", expected="LED ON")
    except Exception as e:
        logging.error(f"Error during ON test: {e}")

    # Test OFF command
    try:
        send_and_log(ser, "OFF", expected="LED OFF")
    except Exception as e:
        logging.error(f"Error during OFF test: {e}")

    logging.info("[Auto Test] Test cycle completed")

def main():
    ser = None
    current_port = None

    logging.info("Waiting for Arduino...")
    while True:
        try:
            detected_port = find_arduino_port()
            if detected_port != current_port:
                # (Dis)connect event
                if ser:
                    logging.info("Arduino disconnected.")
                    ser.close()
                    ser = None
                    current_port = None

                if detected_port:
                    logging.info(f"Arduino detected on {detected_port}")
                    try:
                        ser = serial.Serial(detected_port, 9600, timeout=1)
                        time.sleep(2)
                        while ser.in_waiting:
                            response = ser.readline().decode(errors='ignore').strip()
                            logging.info(f"Arduino: {response}")
                        automated_test(ser)
                        current_port = detected_port
                    except Exception as e:
                        logging.error(f"Error connecting to {detected_port}: {e}")
                        ser = None
                        current_port = None
            time.sleep(1)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()

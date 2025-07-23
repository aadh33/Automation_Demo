import re
import serial
import serial.tools.list_ports

def list_serial_devices():
    """
    Returns a list of (index, port.device, port.description) for serial devices.
    """
    valid_ports = []
    all_ports = serial.tools.list_ports.comports()

    for i, port in enumerate(all_ports):
        if re.search(r'serial', port.description, re.IGNORECASE):
            valid_ports.append((i, port.device, port.description))

    return valid_ports

def select_serial_port():
    devices = list_serial_devices()

    if not devices:
        print(" No USB Serial devices found.")
        return None

    print("\n Available USB Serial Devices:")
    for idx, device, desc in devices:
        print(f"[{idx}] {device} - {desc}")

    while True:
        try:
            choice = int(input("\n Select a device by its number: "))
            selected = next((d for d in devices if d[0] == choice), None)
            if selected:
                print(f"\n Selected: {selected[1]} - {selected[2]}")
                return selected[1]
            else:
                print(" Invalid selection. Try again.")
        except ValueError:
            print(" Please enter a valid number.")

def open_serial_connection(port, baudrate=9600):
    """
    Opens and returns a serial connection.
    """
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        print(f"\n Connected to {port} at {baudrate} baud.\n")
        return ser
    except serial.SerialException as e:
        print(f" Could not open serial port {port}: {e}")
        return None

def echo_serial_messages(serial_conn):
    """
    Echo mode: user types a message, it sends to serial, and reads the response.
    """
    print("🔁 Echo Mode: Type messages to send. Type 'exit' to quit.\n")

    try:
        while True:
            message = input(" You: ")

            if message.lower() == 'exit':
                break
            
            # Append newline (many microcontrollers expect this)
            if not message.endswith('\n'):
                message += '\n'

            # Send message
            serial_conn.write(message.encode())

            # Read and print response (if any)
            response = serial_conn.readline().decode(errors="ignore").strip()
            if response:
                print(f" Echoed: {response}")
            else:
                print(" No response.")

    except Exception as e:
        print(f" Communication error: {e}")

# ===== MAIN PROGRAM =====

if __name__ == "__main__":
    selected_port = select_serial_port()
    
    if selected_port:
        ser = open_serial_connection(selected_port)

        if ser:
            echo_serial_messages(ser)

            ser.close()
            print("\nSerial port closed.")

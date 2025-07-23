import re
import serial
import serial.tools.list_ports

def list_serial_devices():
    """
    List all available serial ports whose description contains 'serial'.
    Return a list of (index, port.device, port.description).
    """
    valid_ports = []
    # List all comports
    all_ports = serial.tools.list_ports.comports()

    for i, port in enumerate(all_ports):
        # Filter for ports containing 'serial' in their description (case-insensitive)
        if re.search(r'serial', port.description, re.IGNORECASE):
            valid_ports.append((i, port.device, port.description))

    return valid_ports

def select_serial_port():
    devices = list_serial_devices()

    if not devices:
        print("No USB Serial devices found.")
        return None

    print("\n🔌 Available USB Serial Devices:")
    for idx, device, desc in devices:
        print(f"[{idx}] {device} - {desc}")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect a device by its number: "))
            selected = next((d for d in devices if d[0] == choice), None)
            if selected:
                print(f"\n✅ Selected: {selected[1]} - {selected[2]}")
                return selected[1]
            else:
                print("⚠️ Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def open_serial_connection(port, baudrate=9600):
    """
    Open and return a Serial connection
    """
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        print(f"\n📡 Connected to {port} at {baudrate} baud.")
        return ser
    except serial.SerialException as e:
        print(f"❌ Could not open serial port {port}: {e}")
        return None

# --- MAIN ---
if __name__ == "__main__":
    selected_port = select_serial_port()
    
    if selected_port:
        ser = open_serial_connection(selected_port)

        if ser:
            try:
                # Example: send data or receive data
                ser.write(b'Hello Device\n')
                response = ser.readline().decode().strip()
                print(f"🧾 Received: {response}")

            except Exception as e:
                print(f"⚠️ Serial I/O error: {e}")
            finally:
                ser.close()
                print("🔒 Serial port closed.")

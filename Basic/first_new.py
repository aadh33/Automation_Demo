import serial.tools.list_ports

def get_ports():
    """Get a list of all available serial ports."""
    return list(serial.tools.list_ports.comports())

def list_ports(ports):
    """Display all available USB serial ports."""
    if not ports:
        print("No serial ports found.")
        return

    print("\nAvailable USB Serial Ports:")
    for i, port in enumerate(ports):
        print(f"{i + 1}: {port.device} - {port.description}")

def find_arduino(ports):
    """Try to automatically find an Arduino among the listed ports."""
    for port in ports:
        if 'USB Serial Port' in port.description or 'Arduino' in port.description:
            return port.device
    return None

# Get all ports
ports_found = get_ports()

# List them for the user
list_ports(ports_found)

# Try to auto-detect Arduino
connect_port = find_arduino(ports_found)

if not connect_port:
    # Ask user to manually select a port
    if ports_found:
        try:
            user_choice = int(input("\nEnter the port number to connect manually (0 to exit): "))
            if user_choice == 0:
                print("Exiting.")
                exit()
            elif 1 <= user_choice <= len(ports_found):
                connect_port = ports_found[user_choice - 1].device
            else:
                print("Invalid choice.")
                exit()
        except ValueError:
            print("Invalid input. Exiting.")
            exit()
    else:
        print("No COM ports found. Exiting.")
        exit()

# Try to connect to the chosen port
try:
    ser = serial.Serial(connect_port, baudrate=9600, timeout=1)
    print(f"\n Connected to Arduino on {connect_port}")
except Exception as e:
    print(f"Failed to connect: {e}")

print("DONE")

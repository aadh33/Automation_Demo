import re
import serial.tools.list_ports

def find_serial_port():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        port_str = str(port)

        
        if re.search(r'usb serial', port_str, re.IGNORECASE):
            match = re.search(r'(COM\d+)', port.device)
            if match:
                return match.group(1)

    return None  


if __name__ == "__main__":
    serial_port = find_serial_port()
    
    if serial_port:
        print(f"Found serial port: {serial_port}")
    else:
        print("No serial port found.")

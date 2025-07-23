import tkinter as tk
import serial.tools.list_ports
import serial

class SerialPortSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Serial Port")
        self.geometry("300x120")
        
        self.selected_port = tk.StringVar(self)
        self.selected_port.set("Select port")
        
        # Get list of available ports
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if not ports:
            ports = ["No ports found"]
        
        # Dropdown menu for COM ports
        self.option_menu = tk.OptionMenu(self, self.selected_port, *ports)
        self.option_menu.pack(pady=10)
        
        # Connect button
        self.connect_button = tk.Button(self, text="Connect", command=self.connect_to_port)
        self.connect_button.pack(pady=5)
        
        self.serial_connection = None

    def connect_to_port(self):
        port = self.selected_port.get()
        if port == "Select port" or port == "No ports found":
            print("Please select a valid port.")
            return
        
        try:
            self.serial_connection = serial.Serial(port, baudrate=9600, timeout=1)
            print(f" Connected to Arduino on {port}")
            self.destroy()  # Close the GUI after successful connection
        except serial.SerialException as e:
            print(f" Failed to connect to {port}: {e}")

if __name__ == "__main__":
    app = SerialPortSelector()
    app.mainloop()
    
    # After GUI closes, serial connection is available as:
    if app.serial_connection and app.serial_connection.is_open:
        # You can now use app.serial_connection here
        # For example:
        # data = app.serial_connection.readline().decode()
        print("Serial port is ready for communication.")
        # Don't forget to close when done
        app.serial_connection.close()
    else:
        print("No serial connection established.")

// Define the application (fake "firmware") version
#define FIRMWARE_VERSION "Arduino UNO R3 Sketch v1.0"

const int ledPin = 13;  // Built-in LED pin

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  // Print version info on boot
  Serial.println(FIRMWARE_VERSION);
  Serial.println("Send 'ON' or 'OFF' via Serial to control LED.");
}

void loop() {
  // Check for serial input
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // Remove leading/trailing whitespace

    if (input.equalsIgnoreCase("ON")) {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED ON");
    } else if (input.equalsIgnoreCase("OFF")) {
      digitalWrite(ledPin, LOW);
      Serial.println("LED OFF");
    } else {
      Serial.println("Unknown command. Use ON or OFF.");
    }
  }
}

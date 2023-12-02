// Define the LED pins
int ledPins[] = {49, 47, 45, 43, 41, 33, 31, 29, 27, 25};
int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

int currentNumLedsToTurnOn = 0;

void setup() {
  // Initialize LED pins as outputs
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if there is serial data available
  if (Serial.available() > 0) {
    // Read the serial input
    int serialInput = Serial.parseInt();

    // Map the serial input value to the number of LEDs to turn on
    currentNumLedsToTurnOn = map(serialInput, 0, 1023, 0, numLeds);

    // Ensure the number of LEDs to turn on is within the valid range
    currentNumLedsToTurnOn = constrain(currentNumLedsToTurnOn, 0, numLeds);
    
    // Consume any remaining characters in the serial buffer
    while (Serial.available() > 0) {
      Serial.read();
    }
  }

  // Turn on the corresponding number of LEDs
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], i < currentNumLedsToTurnOn ? HIGH : LOW);
  }

  delay(100);  // Adjust the delay as needed for smoother response
  // I hate arduino
}

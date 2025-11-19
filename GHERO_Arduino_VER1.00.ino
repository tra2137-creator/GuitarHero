// ==== PIN SETUP ====
const int RED_PIN    = 6;  // sends 'd'
const int GREEN_PIN  = 4;  // sends 'f'
const int BLUE_PIN   = 2;  // sends 'j'
const int YELLOW_PIN = 3;  // sends 'k'
const int PURPLE_PIN = 5;  // sends 'l'

// ==== BUTTON STATE ====
int lastStateRed = HIGH;
int lastStateGreen = HIGH;
int lastStateBlue = HIGH;
int lastStateYellow = HIGH;
int lastStatePurple = HIGH;

void setup() {
  Serial.begin(9600);

  pinMode(RED_PIN, INPUT_PULLUP);
  pinMode(GREEN_PIN, INPUT_PULLUP);
  pinMode(BLUE_PIN, INPUT_PULLUP);
  pinMode(YELLOW_PIN, INPUT_PULLUP);
  pinMode(PURPLE_PIN, INPUT_PULLUP);
}

void loop() {
  checkButton(RED_PIN,    'd', lastStateRed);
  checkButton(GREEN_PIN,  'f', lastStateGreen);
  checkButton(BLUE_PIN,   'j', lastStateBlue);
  checkButton(YELLOW_PIN, 'k', lastStateYellow);
  checkButton(PURPLE_PIN, 'l', lastStatePurple);
}

void checkButton(int pin, char outChar, int &lastState) {
  int current = digitalRead(pin);

  // Button pressed (active LOW)
  if (current == LOW && lastState == HIGH) {
    Serial.println(outChar);
    delay(20); // debounce
  }

  lastState = current;
}

// ==== PIN SETUP ====
const int RED_PIN    = 6;   // sends 'd'
const int GREEN_PIN  = 4;   // sends 'f'
const int BLUE_PIN   = 2;   // sends 'j'
const int YELLOW_PIN = 3;   // sends 'k'
const int PURPLE_PIN = 5;   // sends 'l'

// STRUMBAR AXIS
const int STRUM_PIN = A0;

// JOYSTICK THRESHOLDS
const int STRUM_UP_THRESHOLD = 300;   // < 300 = strum up
const int STRUM_DOWN_THRESHOLD = 700; // > 700 = strum down

bool strum_locked = false;

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

  pinMode(STRUM_PIN, INPUT);
}

void loop() {

  // ==== FRETS ====
  checkButton(RED_PIN,    'd', lastStateRed);
  checkButton(GREEN_PIN,  'f', lastStateGreen);
  checkButton(BLUE_PIN,   'j', lastStateBlue);
  checkButton(YELLOW_PIN, 'k', lastStateYellow);
  checkButton(PURPLE_PIN, 'l', lastStatePurple);

  // ==== STRUMBAR ====
  int val = analogRead(STRUM_PIN);

  // STRUM UP (only once until reset)
  if (val < STRUM_UP_THRESHOLD && !strum_locked) {
    Serial.println("STRUM_UP");
    strum_locked = true;
  }
  // STRUM DOWN
  else if (val > STRUM_DOWN_THRESHOLD && !strum_locked) {
    Serial.println("STRUM_DOWN");
    strum_locked = true;
  }
  // RESET when back to middle
  else if (val >= STRUM_UP_THRESHOLD && val <= STRUM_DOWN_THRESHOLD) {
    strum_locked = false;
  }

  delay(5);
}

void checkButton(int pin, char outChar, int &lastState) {
  int current = digitalRead(pin);

  if (current == LOW && lastState == HIGH) {
    Serial.println(outChar);
    delay(15); // debounce
  }

  lastState = current;
}

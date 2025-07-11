const int button1 = 2;
const int button2 = 3;
bool lastButton1State = LOW;
bool lastButton2State = LOW;

void setup() {
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  bool current1 = digitalRead(button1);
  bool current2 = digitalRead(button2);

  if (current1 == LOW && lastButton1State == HIGH) {
    Serial.println("SET1");
    delay(200); // 디바운스
  }

  if (current1 == HIGH && lastButton1State == LOW) {
    Serial.println("SET2");
    delay(200); // 디바운스
  }

  lastButton1State = current1;
  lastButton2State = current2;
}

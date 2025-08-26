const int LED_PIN = 12;
const int PIR_PIN = 7;

volatile int tot_count = 0;
int greenLedState = LOW;

void checkPresence() {
  greenLedState = !greenLedState;
  digitalWrite(LED_PIN, greenLedState);
  if(digitalRead(PIR_PIN) == HIGH) {
    tot_count++;
  }   
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Lab 1.3 Starting");
  
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), checkPresence, CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Total count: "+(String)tot_count);
  delay(30 * 1e03);
}

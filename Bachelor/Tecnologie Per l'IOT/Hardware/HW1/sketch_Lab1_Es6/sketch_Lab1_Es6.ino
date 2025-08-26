#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd (0x27);
const int TMP_PIN = A1;
const int B = 4275;
const long int R0 = 100000;
const int VCC = 1023;
const float T0 = 298.15;


void setup() {
  // put your setup code here, to run once:
  pinMode(TMP_PIN, INPUT);
  lcd.begin(16,2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
  lcd.print("Temperature:");
}

void loop() {
  // put your main code here, to run repeatedly:
  float v = analogRead(TMP_PIN);
  float t = 1/((float)log((R0*(VCC/v -1))/R0)/B + (float)1/T0) - 273.15;
  lcd.setCursor(12,0);
  lcd.print((String)t);
  delay(5 * 1e03);
}

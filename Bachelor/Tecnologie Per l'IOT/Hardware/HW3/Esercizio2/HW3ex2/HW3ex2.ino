#include <Bridge.h>
#include <Process.h>
#include <String.h>

Process p;

const int K2C = 273.15;
const int B = 4275;
const long R0 = 100000;
const long R1 = 100000;
const int T0 = 25 + K2C;
const int VCC = 1023;
float temp;
const int TEMP_PIN = A0;
const int INT_LED_PIN = 12;

float readTempSensor(){
  return (1/((float) log(R1*((float) VCC/analogRead(TEMP_PIN) - 1)/R0)/B + (float) 1/T0) - K2C);
}


void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Serial initialized!");
  pinMode(TEMP_PIN, INPUT);
  pinMode(INT_LED_PIN, OUTPUT);
  digitalWrite(INT_LED_PIN, LOW);
  Bridge.begin();
  digitalWrite(INT_LED_PIN, HIGH);
  Serial.println("Bridge Initialized!");

  p.begin("python3");
  p.addParameter("/Desktop/PythonScripts/HW3ex2Client.py");
  p.runAsynchronously();
}

void loop() {
  temp = readTempSensor();
  String msg = "T:" + String(temp);
  p.println(msg);
  Serial.print("Sent command: ");
  Serial.println(msg);

  while(p.available() > 0){
    char c = p.read();
    Serial.print(c);
  }
  delay(2000);
}

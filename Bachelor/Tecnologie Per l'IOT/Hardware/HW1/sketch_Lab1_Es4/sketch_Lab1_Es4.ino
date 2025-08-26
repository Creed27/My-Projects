const int FAN_PIN = 11;
float currentSpeed = 0;
const float stepBy = 25.5;

void serialPrintStatus() {
  if(Serial.available() > 0) {
    int inByte = Serial.read();
    if(inByte == '+'){
      if(currentSpeed == 255){
        Serial.println("Maximum speed reached");
      }
      else{
        currentSpeed += stepBy;
        analogWrite(FAN_PIN, currentSpeed);
        Serial.println("Current speed: " + (String)currentSpeed);
      }
    }
    else if(inByte == '-'){
      if(currentSpeed == 0){
        Serial.println("Minimum speed reached");
      }
      else{
        currentSpeed -= stepBy;
        analogWrite(FAN_PIN, currentSpeed);
        Serial.println("Current speed: " + (String)currentSpeed);
        
      }
    }
    else{
      Serial.println("Errore, comando non riconosciuto");
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Lab 1.4 Starting");
  
  pinMode(FAN_PIN, OUTPUT);
  analogWrite(FAN_PIN, currentSpeed);
}

void loop() {
  // put your main code here, to run repeatedly:
  serialPrintStatus();
}

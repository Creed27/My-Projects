#include <math.h>
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd (0x27);

// Costanti per il calcolo della temperatura nella stanza
const int TMP_PIN = A1;
const int B = 4275;
const long int R0 = 100000;
const int VCC = 1023;
const float T0 = 298.15;

// Costanti per il controllo della ventola
const int FAN_PIN = 11;
float currentSpeed = 0;
const int y1V = 0;
const int y2V = 255;

// Costanti per il controllo del LED
const int LED_PIN = 10;
float currentLight = 0;
const int y1L = 255;
const int y2L = 0;

// Costanti per il PIR
const int PIR_PIN = 0;
const unsigned long timeoutPir = 1800000; // è in millisecondi
volatile int movementCount = 0;


// Costanti per il sensore di rumore
const int SND_PIN = 7;
const int nSoundsEvent = 10;
const unsigned long soundInterval = 600000;
const unsigned long timeoutSound = 3600000;
volatile int soundCount = 0;
int totSound = 0;

// Gestione timer e presenza
volatile int presence = 0; 
unsigned long dt1, dt2, dt3, t1 = 0, t2 = 0, t3 = 0;



// Funzioni
void checkValue(float* value){
  if(*value < 0){
    *value = 0;
  }
  else if(*value > 255){
    *value = 255;
  }
}


void checkSounds(){
  soundCount++;
}


void serialCommand() {
  if(Serial.available() > 0) {
    int inByte = Serial.read();
    if(inByte == '1'){
      Serial.println("Hai impostato la PRESENZA di una persona nella stanza");
      presence = 1;
    }
    else if(inByte == '0'){
      Serial.println("Hai impostato l'ASSENZA di persone nella stanza");
      presence = 0;
    }
    else{
      Serial.println("Errore, comando non riconosciuto");
    }
  }
}



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(TMP_PIN, INPUT);
  pinMode(FAN_PIN, OUTPUT);
  analogWrite(FAN_PIN, currentSpeed);
  pinMode(LED_PIN, OUTPUT);
  analogWrite(LED_PIN, currentLight);
  pinMode(PIR_PIN, INPUT);
  pinMode(SND_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(SND_PIN), checkSounds, FALLING);
  lcd.begin(16,2);
  lcd.setBacklight(255);
}

void loop() {
  
  // STEP 1: Calcolo la temperatura nella stanza
  float v = analogRead(TMP_PIN);
  float t = 1/((float)log((R0*(VCC/v -1))/R0)/B + (float)1/T0) - 273.15;

  // STEP 2: Controllo la PRESENZA di persone nella stanza 
  if(digitalRead(PIR_PIN) == HIGH){ 
    movementCount++;
    presence = 1; // Se rilevo un movimento, qualcuno è nella stanza
  }

  dt1 = millis()-t1;
  if(dt1 >= timeoutPir){ // Ogni 30 minuti controllo quanti movimenti sono stati rilevati
    t1 = millis(); // Aggiorno il riferimento temporale
    if(movementCount == 0){
      presence = 0;
    }
    else{
      presence = 1;
    }
    movementCount = 0; // Resetto il counter
  }

  
  dt2 = millis()-t2;
  dt3 = millis()-t3;
  if(dt2 >= soundInterval){ 
    t2 = millis();
    if(soundCount >= nSoundsEvent){ // Se rilevo un numero di eventi superiore a 50 in un intervallo di tempo di 10 minuti, qualcuno è nella stanza
      presence = 1;
    }
    totSound += soundCount; // Aggiorno il numero di eventi degli ultimi 60 minuti
    soundCount = 0;
  }

  if(dt3 >= timeoutSound){ // Passati 60 minuti controllo se ci sono stati abbastanza eventi
    t3 = millis();
    if(totSound == 0){
      presence = 0;
    }
    totSound = 0;
  }

  serialCommand();

 
  int x1V, x2V, x1L, x2L;
  if(presence){
    x1V = 20;
    x2V = 25;
    x1L = 15;
    x2L = 20;
  }
  else{
    x1V = 25;
    x2V = 30;
    x1L = 12;
    x2L = 17;
  }

  
  // STEP 3: Controllo VENTOLA
  int m1 = (y2V-y1V)/(x2V - x1V);
  int q1 = (x1V * (y1V-y2V)/(x2V - x1V))+y1V;
  currentSpeed = m1*t + q1;
  checkValue(&currentSpeed);
  analogWrite(FAN_PIN, currentSpeed);


  // STEP 4: Controllo LED
  int m2 = (y2L-y1L)/(x2L - x1L);
  int q2 = (x1L * (y1L-y2L)/(x2L - x1L))+y1L;
  currentLight = m2*t + q2;
  checkValue(&currentLight);
  analogWrite(LED_PIN, currentLight);

  // STEP 5: Visualizzo valori su display
  lcd.clear();
  lcd.home();
  lcd.print("T:"+(String)t);
  lcd.setCursor(8,0);
  lcd.print("Pres:"+(String)presence);
  lcd.setCursor(0,1);
  int val = currentSpeed * 100 / 255;
  lcd.print("AC:"+(String)val+"%");
  lcd.setCursor(8,1);
  val = currentLight * 100 / 255;
  lcd.print("HT:"+(String)val+"%");
  delay(5 * 1e03);
  lcd.clear();
  lcd.home();
  lcd.print("AC m:"+(String)x1V+" M:"+(String)x2V);
  lcd.setCursor(0,1);
  lcd.print("HT m:"+(String)x1L+" M:"+(String)x2L);
  delay(5 * 1e03);
}

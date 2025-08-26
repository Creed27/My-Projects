#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <String.h>

const int K2C = 273.15;
const int B = 4275;
const long R0 = 100000;
const long R1 = 100000;
const int T0 = 25 + K2C;
const int VCC = 1023;
float temperature;
const int TEMP_PIN = A0;
const int LED_PIN = 13;
BridgeServer server;

String senMlEncode(String resource, int val, String unit){
  String body = "{\n 'bn': 'Yùn'\n 'e': [\n   {\n   'n': " + resource + ",\n   't': " + millis() + ",\n   'v': " + val + ",\n   'u': ";
  if(resource == "temperature"){
    body += "Cel\n   }\n ]\n}";
  } 
  else{
    body += "null\n   }\n ]\n}";
  }
  return body;
}

void printResponse(BridgeClient client, int code, String body){
  client.println("Status: " + String(code));
  if(code == 200){
    client.println(F("Content-type: application/json; charset=utf-8"));
    client.println(); // mandatory blank line
    client.println(body); //the response body
  }
}

void process(BridgeClient client){
  String command = client.readStringUntil('/');
  command.trim();

  if(command == "led"){
    int val = client.parseInt();
    if(val == 0 || val == 1){
      digitalWrite(LED_PIN, val);
      printResponse(client, 200, senMlEncode(F("led"), val, F("")));
    }
    else{
      printResponse(client, 400, "Bad request, parameter val not accepted!");
    }
  }
  else if(command == "temperature"){
    int val = 1/((float) log(R1*((float) VCC/analogRead(TEMP_PIN) - 1)/R0)/B + (float) 1/T0) - K2C;
    printResponse(client, 200, senMlEncode(F("temperature"), val, F("")));
  }
  else{
    printResponse(client, 400, "Bad Request: command does not exists");
  }
}

void setup() {
  pinMode(LED_PIN,OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Bridge.begin();
  digitalWrite(LED_PIN, HIGH);
  pinMode(TEMP_PIN, INPUT);
  server.listenOnLocalhost();
  server.begin();
}

void loop() {
  BridgeClient client = server.accept();
  if (client){
    process(client);
    client.stop();
  }
  delay(50);
}

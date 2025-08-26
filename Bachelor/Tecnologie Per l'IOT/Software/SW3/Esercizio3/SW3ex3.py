import paho.mqtt.client as mqtt
import json
import time
import urllib3

# Client Name
CLIENT_NAME = "MQTTServiceC"
# Number of second between each message
SECOND_BTW_MESSAGES = 1

ipAddress = "192.168.17.50"
port = 8080

id = "ArduinoService"
topic = "tiot/group10/service/command"

def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    print("Connected with code = " + str(rc))

if __name__ == "__main__":
    http = urllib3.PoolManager()
    request = http.request("GET", "http://192.168.17.50:8099/")
    subscription = json.loads(request.data.decode("utf-8"))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(subscription["subscription"]["MQTT"]["device"]["hostname"], subscription["subscription"]["MQTT"]["device"]["port"])
    
    for sub in subscription["subscription"]["MQTT"].keys():
        print(sub)
        print(json.loads(http.request("GET", "http://192.168.17.50:8099/" + sub + "s").data.decode("utf-8")).__str__() + "\n")
    device = {}
    while len(device.keys()) == 0:
        device = json.loads(http.request("GET", "http://192.168.17.50:8099/devices/ledDevice").data.decode("utf-8"))
        time.sleep(5)
    print(str(device) + "\n")  
    endPoint = device["endPoint"]
    print(endPoint + "\n")
    client.loop_start()
    
    jsonData = json.dumps({
            "uuid": "serviceTemeprature",
            "endPoint": "tiot/group4/service/temperature",
            "description": "Information about catalog" 
        }).encode("utf-8")

    lastUpdate = 0
    lastPublish = 0
    state = 0
    while True:          
            if time.time() - lastPublish > 15:
                lastPublish = time.time()
                client.publish(endPoint, json.dumps({"bn": "Yun", "e": [{"n": "led", "t": None, "v": state, "u": None}]}))
                if state == 0:
                    state = 1
                else:
                    state = 0
                print("Led status changed")
            if time.time() - lastUpdate > 60:
                lastUpdate = time.time()
                print(http.request("POST", subscription["subscription"]["REST"]["service"], body = jsonData, headers = {"Content-Type" : "application/service"}).status.__str__())
import paho.mqtt.client as mqtt
import json
import time
import urllib3

def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    print("Connected with code = " + str(rc))
    
def on_message(client, userdata, message):
    msg = message.payload
    print("Temperature: " + str(json.loads(msg)["e"][0]["v"]))
    client.publish("tiot/group4/service/temperature", msg)
    
if __name__ == "__main__":
    http = urllib3.PoolManager()
    request = http.request("GET", "http://192.168.17.50:8099/")
    connectInfo = json.loads(request.data.decode("utf-8"))["subscriptions"]["MQTT"]["device"]
    subscription = json.loads(request.data.decode("utf-8"))
    
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(connectInfo["hostname"], connectInfo["port"])
    
    for sub in subscription["subscription"]["MQTT"].keys():
        print(sub)
        print(json.loads(http.request("GET", "http://192.168.17.50:8099/" + sub + "s").data.decode("utf-8")).__str__() + "\n")
    device = {}
    while len(device.keys()) == 0:
        device = json.loads(http.request("GET", "http://192.168.17.50:8099/devices/temperatureDevice").data.decode("utf-8"))
        time.sleep(10)
    print(str(device) + "\n")
        
    endPoint = device["endPoint"]
    print(endPoint + "\n")
    client.subscribe(endPoint)
    client.loop_start()

    jsonData = json.dumps({
            "uuid": "serviceTemeprature",
            "endPoint": "tiot/group4/service/temperature",
            "description": "Information about catalog" 
        }).encode("utf-8")
    lastUpdate = 0
    while True:          
            if time.time() - lastUpdate > 60:
                lastUpdate = time.time()
                print(http.request("POST", subscription["subscription"]["REST"]["service"], body = jsonData, headers = {"Content-Type" : "application/service"}).status.__str__())
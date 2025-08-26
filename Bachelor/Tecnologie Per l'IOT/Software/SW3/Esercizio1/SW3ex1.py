import paho.mqtt.client as mqtt
import json
import time
import urllib3

MESSAGE = {
    "bn" : "YunGroup4",
    "e" : []
}

MEASURE = {
    "n" : "temperature",
    "t" : 0,
    "v" : 0.0,
    "u" : "Cel"
}

def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    client.subscribe(connect["topic"] + "/temperatureDevice")
    client.subscribe(connect["topic"] + "/ledDevice")
    client.subscribe("tiot/group4/command")
    print("Connected with code = " + str(rc))
    
def on_message(client, userdata, message):
    topic = message.topic.split('/')
    msg = message.payload.decode('utf-8')
    if topic[-1] == 'command':
        msg = json.loads(msg)
        if topic[0] == 'tiot':
            if topic[1] == 'group4':
                if "bn" in msg.keys():
                    if "e" in msg.keys():
                        if "n" in msg["e"][0].keys():
                            if "t" in msg["e"][0].keys():
                                if "v" in msg["e"][0].keys():
                                    if "u" in msg["e"][0].keys():
                                        peripheral = msg["e"][0]["n"]
                                        value = msg["e"][0]["v"]
                                        if peripheral != 'led':
                                            return
                                        print("L:"+str(value))
                                    else:
                                        print("u is missing in the message")
                                else:
                                    print("v is missing in the message")
                            else:
                                print("t is missing in the message")
                        else:
                            print("n is missing in the message")
                    else:
                        print("e is missing in the message")
                else:
                    print("bn is missing in the message")
            else:
                print("topic is not well formatted: wrong group")
        else:
            print("topic is not well formatted")
    elif topic[-1] == "catalog":
        print(msg)



if __name__ == '__main__':
    http = urllib3.PoolManager()
    request = http.request("GET", "http://192.168.17.50:8099/")
    connectInfo = json.loads(request.data.decode("utf-8"))["subscriptions"]["MQTT"]["device"]
    
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(connectInfo["hostname"], connectInfo["port"])
    client.subscribe('tiot/group4/command')
    client.loop_start()
    
    jsonDataT = json.dumps({
        "uuid": "temperatureDevice",
        "endPoint": "tiot/group4/device/temperature",
        "resource": "Temperature"
    }).encode("utf-8")

    jsonDataL = json.dumps({
        "uuid": "ledDevice",
        "endPoint": "tiot/group4/device/led",
        "resource": "Led"
    }).encode("utf-8")
    
    lastUpdate = 0 
    while (True):
        msg = input()
        msg = msg.split(':')
        if msg[0] == 'T':
            try:
                val = float(msg[1].strip())
            except:
                print("Unrecognized message!")
                continue
            MEASURE["t"] = time.time()
            MEASURE["v"] = val
            MESSAGE["e"] = [MEASURE]
            jsonData = json.dumps(MESSAGE).encode('utf-8')
            client.publish('tiot/group4/device/temperature', jsonData)
        else:
            print("Error, command not known")
        if time.time() - lastUpdate > 60:
            lastUpdate = time.time()
            client.publish(connect["topic"], jsonDataT)
            client.publish(connect["topic"], jsonDataL)
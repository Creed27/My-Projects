import paho.mqtt.client as mqtt
import json
import time

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
    else:
        print("topic is not well formatted: command not known")

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('test.mosquitto.org', 1883)
    client.subscribe('tiot/group4/command')
    client.loop_start()
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
            client.publish('/tiot/group4', jsonData)
        else:
            print("Error, command not known")
            
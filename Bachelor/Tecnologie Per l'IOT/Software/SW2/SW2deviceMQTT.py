import time
import json
import paho.mqtt.client as mqtt
import urllib3
import uuid


def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    client.subscribe(connect["topic"] + "/" + uiid)
    print("Connected with code = ", str(rc))

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    print(message)

if __name__ == "__main__":
    http = urllib3.PoolManager()

    lastUpdate = 0
    uuid = str(uuid.uuid1())
    request = http.request("GET", "http://192.168.17.50:8099/")
    connectInfo = json.loads(request.data.decode("utf-8"))["subscriptions"]["MQTT"]["device"]
    endpoint = "/device" + uuid + "/humidity"
    jsonData = json.dumps({
        "uuid": uuid,
        "endPoint": endpoint,
        "resource": "Humidity"
    }).encode("utf-8")

    client = mqtt.Client("deviceMQTT")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(connectInfo["hostname"], connectInfo["port"])
    client.loop_start()

    while True:
        if time.time() - lastUpdate > 60:
            lastUpdate = time.time()
            client.publish(connectInfo["topic"], jsonData)        
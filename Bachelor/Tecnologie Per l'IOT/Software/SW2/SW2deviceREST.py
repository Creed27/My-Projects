import json
import urllib3
import time
import uuid

if __name__ == "__main__":
    http = urllib3.PoolManager()
    uid = str(uuid.uuid1())
    get = http.request("GET", "http://127.0.0.1:8099/") #Retrieve subscription info
    sub = json.loads(get.data.decode("utf-8"))

    deviceInfo = json.dumps({
        "uuid": uid,
        "end-point": "192.168.1.1",
        "availRes": "Temperature"
    }).encode("utf-8")

    while True:
        lastUpdate = 0
        if time.time() - lastUpdate > 60:
            lastUpdate = time.time()
            print(http.request("POST", sub["subscription"]["REST"]["device"], body = deviceInfo, headers = {"Content-Type" : "application/device"}).status.__str__())

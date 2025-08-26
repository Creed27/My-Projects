import json
import urllib3
import time

if __name__ == '__main__':
    http = urllib3.PoolManager()
    while(True):
        msg = input()
        msg = msg.split(':')
        if msg[0] == 'T':
            try:
                val = float(msg[1].strip())
            except:
                print("Cannot convert to float")
                continue
            data = {
                "n" : "temperature",
                "t" : time.time(),
                "v" : val,
                "u" : "Cel"
            }
            jsonData = json.dumps(data).encode('utf-8')
            r = http.request('POST', 'http://192.168.56.1:8099/log', body = jsonData, headers = {'Content-Type' : 'application/json'})
            print(str(r.status))
        else:
            print("Unrecognized message:" + msg)
import json
import cherrypy
import time
import paho.mqtt.client as mqtt


DEVICES = {}
SERVICES = {}
USERS = {}

class Catalog(object):
    exposed = True 
    
    def GET(self, *uri, **params):
        global DEVICES
        global SERVICES
        global USERS
        if len(uri) != 0:
            match uri[0]:
                case 'devices':
                    if len(uri) == 1: #Retrieve devices list URI:.../devices
                        return json.dumps(DEVICES)
                    elif uri[1] in DEVICES.keys(): #Retrieve information of only one specific device URI:.../devices/did
                        return json.dumps(DEVICES[uri[1]])
                    else:
                        raise cherrypy.HTTPError(404, "Bad Request, URI is not correctly formatted. Check specific ID!") 
                            
                case 'services':
                    if len(uri) == 1: #Retrieve sevices list URI:.../services
                        return json.dumps(SERVICES)
                    elif uri[1] in SERVICES.keys(): #Retrieve information of only one specific service URI:.../services/sid
                        return json.dumps(SERVICES[uri[1]])
                    else:
                        raise cherrypy.HTTPError(404, "Bad Request, URI is not correctly formatted. Check specific ID!") 
                
                case 'users':
                    if len(uri) == 1: #Retrieve users list URI:.../users
                        return json.dumps(USERS)
                    elif uri[1] in USERS.keys(): #Retrieve information of only one specific user URI:.../users/sid
                        return json.dumps(USERS[uri[1]])
                    else:
                        raise cherrypy.HTTPError(404, "Bad Request, URI is not correctly formatted. Check specific ID!") 
        else:
            response = {
                "subscriptions" : {
                    "REST" : {
                        "device" : "http://192.168.0.10:8099/devices/subscription",
                        "service" : "http://192.168.0.10:8099/services/subscription",
                         "users" : "http://192.168.0.10:8099/users/subscription"
                    },
                    "MQTT" : {
                        "device" : {
                        "hostname" : "iot.eclipse.org",
                        "port" : "1883",
                        "topic" : "tiot/group4/catalog/devices/subscription"
                        },
                        "service" : {
                        "hostname" : "iot.eclipse.org",
                        "port" : "1883",
                        "topic" : "tiot/group4/catalog/services/subscription"
                        },
                        "users" : {
                        "hostname" : "iot.eclipse.org",
                        "port" : "1883",
                        "topic" : "tiot/group4/catalog/users/subscription"
                        }
                    }
                }
            }
            return json.dumps(response)
            
            
    def POST(self, *uri, **params):
        global DEVICES
        global SERVICES
        global USERS
        if len(uri) == 2 and uri[1] == 'subscription':
            contentlength = cherrypy.request.headers['Content-Length']
            if contentlength:
                rawbody = cherrypy.request.body.read(int(contentlength))
                jsonDict = json.loads(rawbody)
                timestamp = int(time.time())
                if uri[0] == 'devices':
                    if 'uuid' in jsonDict.keys():
                        if 'end-point' in jsonDict.keys():
                            if 'availRes' in jsonDict.keys():
                                if jsonDict['uuid'] in DEVICES.keys(): #It's a refresh of the device
                                    DEVICES[jsonDict['uuid']]['timestamp'] = time.time()
                                else:
                                    DEVICES[jsonDict['uuid']] = {
                                        'DID' : jsonDict['uuid'],
                                        'end-point' : jsonDict['end-point'],
                                        'availRes' : jsonDict['availRes'],
                                        'timestamp' : time.time()
                                    }
                            else:
                                raise cherrypy.HTTPError(404, "Bad Request: availRes is missing in the body")
                        else:
                            raise cherrypy.HTTPError(404, "Bad Request: end-point is missing in the body")
                    else:
                        raise cherrypy.HTTPError(404, "Bad Request: uuid is missing in the body")       
                elif uri[0] == 'services':
                    if 'uuid' in jsonDict.keys():
                        if 'description' in jsonDict.keys():
                            if 'end-point' in jsonDict.keys():
                                if SERVICES[jsonDict['uuid']] in SERVICES.keys(): #Refresh
                                    SERVICES[jsonDict['uuid']][timestamp] = time.time()
                                else:
                                    SERVICES[jsonDict['uuid']] = {
                                        'SID' : jsonDict['uuid'],
                                        'description' : jsonDict['description'],
                                        'end-point' : jsonDict['end-point'],
                                        'timestamp' : time.time()
                                    }
                            else:
                                raise cherrypy.HTTPError(404, "Bad Request: end-point is missing in the body")
                        else:
                            raise cherrypy.HTTPError(404, "Bad Request: description is missing in the body")
                    else:
                        raise cherrypy.HTTPError(404, "Bad Request: uuid is missing in the body")
                else:
                    USERS[jsonDict['uuid']] = {
                        'UID' : jsonDict['uuid'],
                        'name' : jsonDict['name'],
                        'surname' : jsonDict['surname'],
                        'emails' : jsonDict['emails']
                    }
            else:
                raise cherrypy.HTTPError(404, "Bad Request, POST header is not correctly formatted!")
        else:
            raise cherrypy.HTTPError(404, "Bad Request, URI is not correctly formatted!")  
 
 def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    client.subscribe("tiot/group4/catalog/devices/subscription")
    print("Connected with code = ", str(rc))
    
def on_message(client, userdata, message):
    global DEVICES
    global SERVICES
    global USERS
    if message.topic.__str__() == "tiot/group4/catalog/devices/subscription":
        message = json.loads(message.payload.decode("utf-8"))
        if "uuid" in message.keys():
            if "end-point" in message.keys():
                if "availRes" in message.keys():
                    if message["uuid"] in DEVICES.keys():
                        DEVICES[message['uuid']]['timestamp'] = time.time()
                    else:
                        DEVICES[message['uuid']] = {
                            'DID' : message['uuid'],
                            'end-point' : message['end-point'],
                            'availRes' : message['availRes'],
                            'timestamp' : time.time()
                            }
                else:
                    raise cherrypy.HTTPError(404, "Bad Request: availRes is missing")
            else:
                raise cherrypy.HTTPError(404, "Bad Request: endpoint is missing")
        else:
            raise cherrypy.HTTPError(404, "Bad Request: uuid is missing")
        client.publish("tiot/group4/catalog/devices/subscription/" + str(message["uuid"]), "200 OK")
        
if __name__ == "__main__":
    global DEVICES
    global SERVICES
    global USERS
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
        }
    }
    cherrypy.tree.mount(Catalog(), "/", conf)

    cherrypy.config.update({"server.socket_host": "127.0.0.1"})
    cherrypy.config.update({"server.socket_port": 8099})

    client = mqtt.Client('Resource Catalog')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mqtt.eclipseprojects.io", 1883)
    client.loop_start()
    
    cherrypy.engine.start()
    while True:
        time.sleep(0.5)
        for did in DEVICES.keys():
            deleteKey = []
            if time.time() - float(DEVICES[did]["timestamp"]) > 120:
                deleteKey.append(did)
            for key in deleteKey:
                DEVICES.pop(key)
                client.unsubscribe("tiot/group4/catalog/" + str(key))
        for sid in SERVICES.keys():
            deleteKey = []
            if time.time() - float(SERVICES[sid]["timestamp"]) > 120:
                deleteKey.append(sid)
            for key in deleteKey:
                SERVICES.pop(key)
                client.unsubscribe("tiot/group4/catalog/" + str(key))
    cherrypy.engine.block()
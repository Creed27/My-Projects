import json
import cherrypy
import time

DATAS =  {
    "bn" : "Yùn",
    "e" : []
}
def POST(self, *uri, **params):
    global DATAS
    if len(uri) == 0:
        contentlength = cherrypy.request.headers['Content-Length']
        if contentlength:
            rawbody = cherrypy.request.body.read(int(contentlength))
            jsonDict = json.loads(rawbody)
            if "n" in jsonDict.keys():
                if "t" in jsonDict.keys():
                    if "v" in jsonDict.keys():
                        if "u" in jsonDict.keys():
                            DATAS["e"].append(jsonDict)
                        else:
                            raise cherrypy.HTTPError(400, "Bad Request: u is missing in the body")
                    else:
                        raise cherrypy.HTTPError(400, "Bad Request: v is missing in the body")
                else:
                    raise cherrypy.HTTPError(400, "Bad Request: t is missing in the body")
            else:
                raise cherrypy.HTTPError(400, "Bad Request: n is missing in the body")
        else:
            raise cherrypy.HTTPError(400, "Bad Request, POST header is not correctly formatted!")
    else:
        raise cherrypy.HTTPError(400, "Bad Request, URI is not correctly formatted!")
        
        
def GET(self, *uri, **params):
    global DATAS
    if len(uri) == 1 and uri[0] == 'datas': #the URI should be something like http:://<PC IP Address>:<port>/log/datas
        return json.dumps(DATAS["e"])
    else:
        raise cherrypy.HTTPError(400, "Bad Request, URI is not correctly formatted!")


if __name__ == '__main__':
    conf={
        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tool.session.on':True
        }
    }
    cherrypy.tree.mount(Converter(),'/log',conf) #Demando il controllo totalmente a cherrypy.
    
    cherrypy.config.update({'server.socket_host' : '192.168.56.1'})
    cherrypy.config.update({'server.socket_port' : 8099})
    
    cherrypy.engine.start()
    cherrypy.engine.block()
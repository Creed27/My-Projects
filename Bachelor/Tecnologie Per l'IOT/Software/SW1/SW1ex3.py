import cherrypy
import json
import time

CONVERSIONS = [] #Lista salvata dal web service
class Converter(object):
    exposed=True
    
    def POST(self, *uri, **params):
        global CONVERSIONS
        contentlength = cherrypy.request.headers['Content-Length']
        if contentlength:
            rawbody = cherrypy.request.body.read(int(contentlength))
            jsonDict = json.loads(rawbody)
            if 'values' in jsonDict.keys():
                if 'originalUnit' in jsonDict.keys():
                    if 'targetUnit' in jsonDict.keys():
                        if jsonDict['originalUnit'] in ['C', 'F', 'K']:
                            if jsonDict['targetUnit'] in ['C', 'F', 'K']:
                                try:
                                    convList = []
                                    for oV in jsonDict["values"]:
                                        oV = float(oV)
                                        match jsonDict["originalUnit"], jsonDict["targetUnit"]:
                                            case 'C', 'K':
                                                convList.append(oV + 273.15)
                    
                                            case 'C', 'F':
                                                convList.append(oV * 9/5 + 32)

                                            case 'K', 'C':
                                                convList.append(oV - 273.15)
                    
                                            case 'K', 'F':
                                                convList.append((oV - 273.15) * 9/5 + 32)
                
                                            case 'F', 'C':
                                                convList.append((oV - 32) * 5/9)
                    
                                            case 'F', 'K':
                                                convList.append((oV - 32) * 5/9 + 273.15)
                                    response = {
                                        'values' : jsonDict['values'],
                                        'originalUnit' : jsonDict['originalUnit'],
                                        'convertedValues' : convList,
                                        'targetUnit' : jsonDict['targetUnit'],
                                        'timestamp' : int(time.time())
                                    }
                                    jsonResponse = json.dumps(response)
                                    CONVERSIONS.append(jsonResponse)
                                    print(CONVERSIONS)
                                    return jsonResponse
                                except:
                                    raise cherrypy.HTTPError(404, "Bad Request, one of the values in the list is not a number!")
                            else:
                                raise cherrypy.HTTPError(404, "Bad Request, targetUnit is not available!")
                        else:
                            raise cherrypy.HTTPError(404, "Bad Request, originalUnit is not available!")
                    else:
                        raise cherrypy.HTTPError(404, "Bad Request, parameter targetUnit is missing!")
                else:
                    raise cherrypy.HTTPError(404, "Bad Request, parameter originalUnit is missing!")
            else:
                raise cherrypy.HTTPError(404, "Bad Request, parameter values is missing!")
        else:
            raise cherrypy.HTTPError(404, "Bad Request, POST header is not correctly formatted!")

if __name__ == '__main__':
    conf={
        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tool.session.on':True
        }
    }
    cherrypy.tree.mount(Converter(),'/',conf) 
    
    cherrypy.config.update({'server.socket_host' : '127.0.0.1'})
    cherrypy.config.update({'server.socket_port' : 8099})
    
    cherrypy.engine.start()
    cherrypy.engine.block()
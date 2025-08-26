import cherrypy
import json

class Converter(object):
    exposed=True
    
    def GET(self, *uri, **params):
        if len(uri) == 3 and len(params) == 0:
            if uri[1] in ['C', 'F', 'K']:
                if uri[2] in ['C', 'F', 'K']:
                    try:
                        value = float(uri[0])
                        match uri[1], uri[2]:
                            case 'C', 'K':
                                convertedValue = value + 273.15
                                            
                            case 'C', 'F':
                                convertedValue = value * 9/5 + 32

                            case 'K', 'C':
                                convertedValue = value - 273.15
                                            
                            case 'K', 'F':
                                convertedValue = (value - 273.15) * 9/5 + 32
                                        
                            case 'F', 'C':
                                convertedValue = (value - 32) * 5/9
                                            
                            case 'F', 'K':
                                convertedValue = (value - 32) * 5/9 + 273.15
                        response = {
                            'value' : uri[0],
                            'originalUnit' : uri[1],
                            'targetUnit' : uri[2],
                            'convertedValue' : convertedValue    
                        }
                        return json.dumps(response)
                    except:
                        raise cherrypy.HTTPError(404, "Bad Request, value is not a number!")
                else:
                    raise cherrypy.HTTPError(404, "Bad Request, targetUnit is not available!")
            else:
                raise cherrypy.HTTPError(404, "Bad Request, originalUnit is not available!")
        else:
            raise cherrypy.HTTPError(404, "Bad Request, URI is not well formatted!")


if __name__ == '__main__':
    conf={
        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tool.session.on':True
        }
    }
    cherrypy.tree.mount(Converter(),'/converter',conf) #Imponendo che la root della URI sia /converter, demando il controllo di quest'ultima totalmente a cherrypy.
    
    cherrypy.config.update({'server.socket_host' : '127.0.0.1'})
    cherrypy.config.update({'server.socket_port' : 8099})
    
    cherrypy.engine.start()
    cherrypy.engine.block()
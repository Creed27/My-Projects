import cherrypy
import json

class Converter(object):
    exposed=True
    
    def GET(self, *uri, **params):
        if len(uri) == 0:
            if 'value' in params.keys():
                if 'originalUnit' in params.keys():
                    if 'targetUnit' in params.keys():
                        if params['originalUnit'] in ['C', 'F', 'K']:
                            if params['targetUnit'] in ['C', 'F', 'K']:
                                try:
                                    value = float(params['value'])
                                    match params["originalUnit"], params["targetUnit"]:
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
                                        'value' : params['value'],
                                        'originalUnit' : params['originalUnit'],
                                        'targetUnit' : params['targetUnit'],
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
                        raise cherrypy.HTTPError(404, "Bad Request, parameter targetUnit is missing!")
                else:
                    raise cherrypy.HTTPError(404, "Bad Request, parameter originalUnit is missing!")
            else:
                raise cherrypy.HTTPError(404, "Bad Request, parameter value is missing!")
        else:
            raise cherrypy.HTTPError(404, "Bad Request, URI is not correctly formatted!")


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
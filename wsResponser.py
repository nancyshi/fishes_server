from TornadoService import TornadoService
import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.escape
from dataMgr import dataMgr
from configMgr import configsDict
from gameLogic import gameLogic

class BaseSocketHandller(WebSocketHandler):
    def getJsonArgument(self,name,default = None):
        args = tornado.escape.json_decode(self.request.body)
        name = tornado.escape.to_unicode(name)
        if name in args:
            return args[name]
        elif default is not None:
            return default
        else:
            raise tornado.web.MissingArgumentError(name)


class WsHandller(BaseSocketHandller):
    playerId = None
    def on_message(self):
        messageType = self.getJsonArgument("type")
        if messageType == "login":
            token = self.getJsonArgument("token")
            uid = dataMgr.login(token)
            self.playerId = uid
            data = dataMgr.queryInitData(uid,configsDict)  
            dic = {
                "type": "login",
                "data": data
            }
            self.write_message(dic)

        elif messageType == "catchFish":
            fishId = self.getJsonArgument("fishId")
            if self.playerId != None :
                gameLogic.catchFish(self.playerId,fishId)
                dic = {
                    "type": "catchFish",
                    "currentDollor": dataMgr.getPlayerDataById(self.playerId).currentDollor
                }
                self.write_message(dic)

        
            
    def check_origin(self,origin):
        return True

wsResponser = TornadoService([
    (r"/",WsHandller),
])
          

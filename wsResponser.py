from TornadoService import TornadoService
import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.escape
from dataMgr import dataMgr
from configMgr import configsDict
from gameLogic import gameLogic
import json

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
    def on_message(self,message):
        
        messageDic = json.loads(message)
        messageType = messageDic["type"]
        if messageType == "login":
            token = messageDic["token"]
            uid = dataMgr.login(token)
            self.playerId = uid
            data = dataMgr.queryInitData(uid,configsDict)  
            dic = {
                "type": "login",
                "data": data
            }
            jsonStr = json.dumps(dic)
            self.write_message(jsonStr)

        elif messageType == "catchFish":
            fishId = messageDic["fishId"]
            if self.playerId != None :
                gameLogic.catchFish(self.playerId,fishId)
                dic = {
                    "type": "catchFish",
                    "currentDollor": dataMgr.getPlayerDataById(self.playerId).currentDollor
                }
                jsonStr = json.dumps(dic)
                self.write_message(jsonStr)

        
            
    def check_origin(self,origin):
        return True

wsResponser = TornadoService([
    (r"/",WsHandller),
])
          

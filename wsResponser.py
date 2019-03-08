from TornadoService import TornadoService
import tornado.web
from tornado.websocket import WebSocketHandler
import tornado.escape
from dataMgr import dataMgr
from configMgr import configsDict
from gameLogic import gameLogic
import json
from intensify import intensify

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

        elif messageType == "changeArea":
            areaId = messageDic["areaId"]
            gameLogic.changeArea(self.playerId,areaId)
            data = dataMgr.queryInitData(self.playerId,configsDict)
            dic = {
                "type": "changeArea",
                #"currentDollor": dataMgr.getPlayerDataById(self.playerId).currentDollor,
                #"currentAreaLevel": dataMgr.getPlayerDataById(self.playerId).currentAreaLevel
                "data": data
            }
            jsonStr = json.dumps(dic)
            self.write_message(jsonStr)

        elif messageType == "intensifyBoat":
            intensifyType = messageDic["intensifyType"]
            intensify.boatIntensify(self.playerId,intensifyType)
            dic = {
                "type": "intensifyBoat",
                "data": "success"
            }
            jsonStr = json.dumps(dic)
            self.write_message(jsonStr)
    def on_close(self):
         if dataMgr.datas.get(self.playerId) != None:
             dataMgr.datas.pop(self.playerId)
         
            
    def check_origin(self,origin):
        return True

wsResponser = TornadoService([
    (r"/",WsHandller),
])
          

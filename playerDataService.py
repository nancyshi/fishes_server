from dataMgr import dataMgr
from configMgr import configsDict
import requestTypeEnum
import json
from Service import Service


class PlayerDataService(Service):
    def __init__(self):
        super().__init__()
        self.port = self.ports["playerDataService"]
    def handller(self,sock,addr):
        backMessageHeader = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n"

        data = sock.recv(1024)
        try:
            header, requestType, playerId, requestBody = self.splitData(data)
        except:
            backMessageHeader = "HTTP/1.1 600 InvalidData\r\nAccess-Control-Allow-Origin: *\r\n\r\n"
            backMessage = backMessageHeader + "InvalidData"
            sock.send(bytes(backMessage,"utf-8"))
            sock.close()
            print("%s received some invalid data , which is %s" % (self.__class__.__name__,data))
            return
        if requestType == requestTypeEnum.PlayerDataReqType.getInitData.value:
            jsonData = dataMgr.queryInitData(playerId,configsDict)
            jsonData = backMessageHeader + jsonData
            sock.send(bytes(jsonData,"utf-8"))
        elif requestType == requestTypeEnum.PlayerDataReqType.updatePlayerData.value:
            dic = json.loads(requestBody)
            dataMgr.updatePlayerData(dic)
            backMessage = backMessageHeader + "successfully updated"
            sock.send(bytes(backMessage,"utf-8"))
        else:
            pass
        sock.close()


playerDataService = PlayerDataService()

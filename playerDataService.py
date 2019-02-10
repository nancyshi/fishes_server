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
        # data = data.decode("utf-8")

        # splitedData = data.split("\r\n\r\n")
        # if len(splitedData) != 3:
        #     print("playerDataService erro: received an invalid data from %s" % addr)
        #     return
        # header, requestInfo, requestBody = splitedData

        # splitedRequestInfo = requestInfo.split("\r\n")
        # if len(splitedRequestInfo) != 2:
        #     print("playerDataService erro: received an invalid requestInfo from %s" % addr)
        #     return
        # requestType, playerId = splitedRequestInfo
        header, requestType, playerId, requestBody = self.splitData(data)
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

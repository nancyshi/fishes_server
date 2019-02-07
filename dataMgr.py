import json
import configMgr
class PlayerData(object):

    def __init__(self, id):
        self.id = id
        self.currentDollor = 100
        self.currentAreaLevel = 1
        self.boatLevel = 1
    def setupPlayerDataFromDB(self):
        pass
    def exchangeToDic(self):
        dic = {}
        dic["id"] = self.id
        dic["currentDollor"] = self.currentDollor
        dic["currentAreaLevel"] = self.currentAreaLevel
        dic["boatLevel"] = self.boatLevel
        return dic

class DataMgr(object):
    
    def __init__(self):
        self.datas = {}
    def queryInitData(self,playerId,configsDict):
        #get player data
        if self.datas.get(playerId) == None:
            onePlayerData = PlayerData(playerId)
            onePlayerData.setupPlayerDataFromDB()
            self.datas[playerId] = onePlayerData
        playerData = self.datas[playerId]
        #get needed fishes data
        neededFishesData = self.getNeededFishesConfig(playerData,configsDict)

        resultDic = {}
        resultDic["playerData"] = playerData.exchangeToDic()
        resultDic["neededFishesData"] = neededFishesData
        jsonStr = json.dumps(resultDic,indent=4)
        return jsonStr

    def getSpecificRulesByAreaLevel(self,givenAreaLevel,refreshRules):
        for element in refreshRules:
            if element["areaId"] == givenAreaLevel:
                return element["rules"]

    def getOneNeededFishConfig(self,givenFishId,fishConfig):
        for element in fishConfig:
            if element["fishId"] == givenFishId:
                return  element
    def getNeededFishesConfig(self,playerData,configsDict):
        areaLevel = playerData.currentAreaLevel
        refreshRules = configsDict["configs/refreshRuleConfig.json"]
        specificRules = self.getSpecificRulesByAreaLevel(areaLevel,refreshRules)
        
        fishConfig = configsDict["configs/fishConfig.json"]
        neededFishesConfig = []
        for element in specificRules:
            resultDic = {}
            resultDic["fishId"] = element["fishId"]
            resultDic["probability"] = element["probability"]
            resultDic["timeDelta"] = element["timeDelta"]
            configDic = self.getOneNeededFishConfig(element["fishId"],fishConfig)
            resultDic["fishModelName"] = configDic["fishModelName"]
            resultDic["basicDollor"] = configDic["fishDollor"]
            currentDollor = self.getCurrentFishDollorByFishId(element["fishId"],configDic["fishDollor"],playerData)
            resultDic["currentDollor"] = currentDollor
            neededFishesConfig.append(resultDic)
        return neededFishesConfig

    def getCurrentFishDollorByFishId(self,givenFishId,basicDollor,playerData):
        return basicDollor * 10
            

dataMgr = DataMgr()
from dataMgr import dataMgr
from configMgr import configsDict

class GameLogic(object):
    def catchFish(self,playerId,*fishIds):
        playerData = dataMgr.getPlayerDataById(playerId)
        neededFishesData = dataMgr.getNeededFishesConfig(playerData,configsDict)

        for oneFishId in fishIds:

            for oneFishData in neededFishesData:
                if oneFishData["fishId"] == oneFishId:
                    currentFishDollor = oneFishData["currentDollor"]
                    dicForUpdate = {
                        "id":playerId,
                        "currentDollor": playerData.currentDollor + currentFishDollor
                    }
                    dataMgr.updatePlayerData(dicForUpdate)
                    break

    def changeArea(self,playerId,areaId):
        playerData = dataMgr.getPlayerDataById(playerId)
        currentAreaLevel = playerData.currentAreaLevel
        currentDollor = playerData.currentDollor
        if areaId == currentAreaLevel + 1:
            nextAreaEnterDollor = dataMgr.getNextEnterDollorByPlayerId(playerId)
            if currentDollor - nextAreaEnterDollor >= 0 :
                currentDollor = currentDollor - nextAreaEnterDollor
                currentAreaLevel = currentAreaLevel + 1

                dic = {
                    "id": playerId,
                    "currentDollor": currentDollor,
                    "currentAreaLevel": currentAreaLevel
                }
                dataMgr.updatePlayerData(dic)
                

                

gameLogic = GameLogic()
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

gameLogic = GameLogic()
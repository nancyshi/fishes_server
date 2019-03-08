from dataMgr import dataMgr
from configMgr import configsDict
class Intensify(object):
    def boatIntensify(self,playerId,intensifyType):
        playerData = dataMgr.getPlayerDataById(playerId)
        boatIntensifyConfigs = configsDict["configs/boatIntensifyConfig.json"]
        
        if intensifyType == "fishRod":
            neededDollor = None
            fishRodLevel = playerData.fishRodLevel
            for oneConfig in boatIntensifyConfigs:
                targetLevel = fishRodLevel + 1
                if oneConfig["fetureType"] == "fishRod":
                    if oneConfig["level"] == targetLevel:
                        neededDollor = oneConfig["neededDollor"]
                        break
            if playerData.currentDollor - neededDollor >= 0:
                currentDollor = playerData.currentDollor - neededDollor
                dic = {
                    "id": playerId,
                    "currentDollor": currentDollor,
                    "fishRodLevel": playerData.fishRodLevel + 1
                }
                dataMgr.updatePlayerData(dic)
        elif intensifyType == "fishFood":
            neededDollor = None
            fishFoodLevel = playerData.fishFoodLevel
            for oneConfig in boatIntensifyConfigs:
                targetLevel = fishFoodLevel + 1
                if oneConfig["fetureType"] == "fishFood":
                    if oneConfig["level"] == targetLevel:
                        neededDollor = oneConfig["neededDollor"]
                        break
            if playerData.currentDollor - neededDollor >= 0:
                currentDollor = playerData.currentDollor - neededDollor
                dic = {
                    "id": playerId,
                    "currentDollor": currentDollor,
                    "fishFoodLevel": playerData.fishFoodLevel + 1
                }
                dataMgr.updatePlayerData(dic)
        elif intensifyType == "fishValueLevel":
            neededDollor = None
            fishValueLevel = playerData.fishValueLevel
            for oneConfig in boatIntensifyConfigs:
                targetLevel = fishValueLevel + 1
                if oneConfig["fetureType"] == "fishValue":
                    if oneConfig["level"] == targetLevel:
                        neededDollor = oneConfig["neededDollor"]
                        break
            if playerData.currentDollor - neededDollor >= 0:
                currentDollor = playerData.currentDollor - neededDollor
                dic = {
                    "id": playerId,
                    "currentDollor": currentDollor,
                    "fishValueLevel": playerData.fishValueLevel + 1
                }
                dataMgr.updatePlayerData(dic)
        
    
intensify = Intensify()
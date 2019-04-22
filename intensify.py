#from dataMgr import dataMgr
from configMgr import configsDict
class Intensify(object):
    def boatIntensify(self,playerId,intensifyType,dataMgr):
        playerData = dataMgr.getPlayerDataById(playerId)
        boatIntensifyConfigs = configsDict["configs/boatIntensifyConfig.json"]
        
        if intensifyType == "fishRod":
            neededDollor = None
            fishRodLevel = playerData.fishRodLevel
            for oneConfig in boatIntensifyConfigs:
                targetLevel = fishRodLevel + 1
                if oneConfig["intensifyType"] == "fishRod":
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
                if oneConfig["intensifyType"] == "fishFood":
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
                if oneConfig["intensifyType"] == "fishValue":
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


    def getClientBoatIntensifyInfoById(self,playerId,dataMgr):
        # client info will include the boatIntensify type , max level of each type, and 
        # needed dollor of next level
        playerData = dataMgr.getPlayerDataById(playerId)
        boatIntensifyConfigs = configsDict["configs/boatIntensifyConfig.json"]
        
        intensifyTypes = []
        for oneConfig in boatIntensifyConfigs:
            if oneConfig["boatLevel"] == playerData.boatLevel:
               if oneConfig["intensifyType"] not in intensifyTypes:
                   intensifyTypes.append(oneConfig["intensifyType"])

        maxLevels = []
        neededDollors = []
        currentLevels = []
        descriptions = []
        for oneType in intensifyTypes:
            maxLevel = 0
            for oneConfig in boatIntensifyConfigs:
                if oneConfig["boatLevel"] == playerData.boatLevel and oneConfig["intensifyType"] == oneType:
                    if oneConfig["level"] > maxLevel:
                        maxLevel = oneConfig["level"]
                    if oneType == "fishRod" and oneConfig["level"] == playerData.fishRodLevel + 1:
                        neededDollors.append(oneConfig["neededDollor"])
                    elif oneType == "fishFood" and oneConfig["level"] == playerData.fishFoodLevel + 1:
                        neededDollors.append(oneConfig["neededDollor"])
                    elif oneType == "fishValue" and oneConfig["level"] == playerData.fishValueLevel + 1:
                        neededDollors.append(oneConfig["neededDollor"])

                    if oneType == "fishRod" and oneConfig["level"] == playerData.fishRodLevel:
                        currentLevels.append(oneConfig["level"])
                        descriptions.append(oneConfig["desc"])

                    elif oneType == "fishFood" and oneConfig["level"] == playerData.fishFoodLevel:
                        currentLevels.append(oneConfig["level"])
                        descriptions.append(oneConfig["desc"])

                    elif oneType == "fishValue" and oneConfig["level"] == playerData.fishValueLevel:
                        currentLevels.append(oneConfig["level"])
                        descriptions.append(oneConfig["desc"])
                        
            maxLevels.append(maxLevel)
        results = []
        for index in range(0,len(intensifyTypes)):
            dic = {
                "intensifyType": intensifyTypes[index],
                "maxLevel": maxLevels[index],
                "nextLevelNeededDollor": neededDollors[index],
                "currentLevel": currentLevels[index],
                "description": descriptions[index]
            }
            results.append(dic)

        return results
intensify = Intensify()
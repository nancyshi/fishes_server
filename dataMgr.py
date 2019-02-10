import json
import configMgr
import sqlite3
class PlayerData(object):

    def __init__(self, id):
        self.id = id
        self.currentDollor = 100
        self.currentAreaLevel = 1
        self.boatLevel = 1
    def setupPlayerDataFromDB(self):
        conn = sqlite3.connect("fish.db")
        cursor = conn.cursor()

        #search if there is one record of given playerId
        cursor.execute("select * from user where id = ?",(self.id,))
        playerDBData = cursor.fetchall()
        if len(playerDBData) >= 1:
            playerDBData = playerDBData[0]
            self.currentDollor = playerDBData[1]
            self.currentAreaLevel = playerDBData[2]
            self.boatLevel = playerDBData[3]
        else:
            print("there is no filted record of player data ")
        cursor.close()
        conn.commit()
        conn.close()


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
        
        playerData = self.getPlayerDataById(playerId)
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

    def getPlayerDataById(self,playerId):
        if self.datas.get(playerId) == None:
            onePlayerData = PlayerData(playerId)
            onePlayerData.setupPlayerDataFromDB()
            self.datas[playerId] = onePlayerData
        playerData = self.datas[playerId]
        return playerData
            
    def updatePlayerData(self,dataDic):
        playerId = dataDic["id"]
        playerData = self.getPlayerDataById(playerId)
        for key in dataDic:
            if key == "id":
                pass
            elif key == "currentDollor":
                playerData.currentDollor = int(dataDic[key])
            elif key == "currentAreaLevel":
                playerData.currentAreaLevel = int(dataDic[key])
            elif key == "boatLevel":
                playerData.boatLevel = int(dataDic[key])
            else:
                print("erro in updatePlayerData: wrong key of dataDic %s" % key)
        
    def checkDBInfo(self):
        conn = sqlite3.connect("fish.db")
        cursor = conn.cursor()
        sqlCheckTableExist = "select tbl_name from sqlite_master where type = ? and name = ?" 
        sqlCreatUser = "create table user(id int primary key, currentDollor int, currentAreaLevel int,boatLevel int)"
        cursor.execute(sqlCheckTableExist,("table","user"))
        values = cursor.fetchall()
        if len(values) >= 1 :
            #user table exist
            print("user table exist")
        else:
            cursor.execute(sqlCreatUser)   
            print("creat user table")
        cursor.close()
        conn.close()
        return True  

    def writePlayerDataToDB(self):
        conn = sqlite3.connect("fish.db")
        cursor = conn.cursor()
        for key,value in self.datas.items():
            #key: playerId   value: playerData
            cursor.execute("select * from user where id = ?",(value.id,))
            resultNum = cursor.fetchall()
            resultNum = len(resultNum)
            if resultNum >= 1:
                #there is already have a record of this player
                cursor.execute("update user set currentDollor = ? , currentAreaLevel = ? , boatLevel = ? where id = ?",(value.currentDollor,value.currentAreaLevel,value.boatLevel,value.id))
                print("update a record")
            else:
                #just don't have a record of this player
                cursor.execute("insert into user values (? , ? , ? , ?)",(value.id,value.currentDollor,value.currentAreaLevel,value.boatLevel))
                print("insert a record")
        cursor.close()
        conn.commit()
        conn.close()
     

dataMgr = DataMgr()
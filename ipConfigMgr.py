#load ipconfig.json

import json
def loadIPConfig():
    with open("ipconfig.json","r") as f:
        dic = json.load(f)
        return dic

ipConfigMgr = loadIPConfig() 
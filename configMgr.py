#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Houwan.Sek"

import os
import json

def loadOneConfigFile(configPath):
    with open(configPath,"r") as f:
        loadDic = json.load(f)
        return loadDic

def getAllConfigFilePath():
    configFilePaths = []
    for root , dirs , files in os.walk("configs"):
        for oneFile in files:
            if root == "configs":
                oneFileName = root + "/" + oneFile
            else:
                oneFileName = "configs/" + root + "/" + oneFile 
            configFilePaths.append(oneFileName)
    return configFilePaths

def loadAllConfigFiles():
    resultDic = {}
    configFilePaths = getAllConfigFilePath()
    for onePath in configFilePaths:
        resultDic[onePath] = loadOneConfigFile(onePath)
    
    return resultDic


configsDict = loadAllConfigFiles()
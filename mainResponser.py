#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Houwan.Sek"

import socket
import threading
import configMgr
import dataMgr
from enum import Enum
import json

IPCONFIG = "127.0.0.1"
PORT = 8000


class RequestTypeEnum(Enum):
    getInitData = "GID"
    updatePlayerData = "UPD"
    login = "LOIN"

def tcplinkHandler(sock,addr,dataMgr,configsDict):
    backMessageHeader = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n"
    data = sock.recv(2048)
    splitedData = data.split(bytes("\r\n\r\n","utf-8"))
    if len(splitedData) == 3:
        header, requestInfo, requestBody = splitedData
    elif len(splitedData) == 2:
        header, requestInfo = splitedData
    else:
        print("invalid data")
        sock.close()
        return
    # header, requestInfo, requestBody = data.split(bytes("\r\n\r\n","utf-8"))
    splitedRequestInfo = requestInfo.split(bytes("\r\n","utf-8"))
    if len(splitedRequestInfo) == 2:
        requestType , playerId = splitedRequestInfo
    else:
        print("invalid requestInfo , which is %s" % splitedRequestInfo)
        sock.close()
        return
    requestType = requestType.decode("utf-8")
    playerId = playerId.decode("utf-8")
    playerId = int(playerId)
    print("request type is %s , playerId is %s" % (requestType,playerId))
    if requestType == RequestTypeEnum.getInitData.value:
        jsonData = dataMgr.queryInitData(playerId,configsDict)
        jsonData = backMessageHeader + jsonData
        sock.send(bytes(jsonData,"utf-8"))
        
    elif requestType == RequestTypeEnum.updatePlayerData.value:
        requestBody = requestBody.decode("utf-8")
        dataDic = json.loads(requestBody,"utf-8")
        dataMgr.updatePlayerData(dataDic)
        backMessage = backMessageHeader + "Successfully updated"
        sock.send(bytes(backMessage,"utf-8"))
    else:
        pass
    sock.close()
    
    

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IPCONFIG,PORT))
s.listen()
print("server now start at %s,%s" % (IPCONFIG,PORT))

configsDict = configMgr.configsDict
dataCenter = dataMgr.dataMgr
dataCenter.checkDBInfo()




def call():
    dataCenter.writePlayerDataToDB()
    time = threading.Timer(10,call)
    time.start()

timer = threading.Timer(10,call)
timer.start()
while True:
    sock, addr = s.accept()
    #print('someone get connected, add: %s, %s' % addr)
    t = threading.Thread(target= tcplinkHandler,args=(sock,addr,dataCenter,configsDict))
    t.start()


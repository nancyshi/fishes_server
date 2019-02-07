#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Houwan.Sek"

import socket
import threading
import configMgr
import dataMgr

IPCONFIG = "127.0.0.1"
PORT = 8000


def tcplinkHandler(sock,addr,dataMgr,configsDict):
    data = sock.recv(1024)
    header,contenData = data.split(bytes("\r\n\r\n","utf-8"),1)
    if(contenData.decode("utf-8") == "request init data"):
        playerId = 10001
        jsonData = dataMgr.queryInitData(playerId,configsDict)
        sock.send(bytes(jsonData,"utf-8"))
    else:
        print("not correct contenData , reveived data is %s" % contenData.decode("utf-8"))
    sock.close()
    
    

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IPCONFIG,PORT))
s.listen()
print("server now start at %s,%s" % (IPCONFIG,PORT))

configsDict = configMgr.configsDict
dataCenter = dataMgr.dataMgr
while True:
    sock, addr = s.accept()
    print('someone get connected, add: %s, %s' % addr)
    t = threading.Thread(target= tcplinkHandler,args=(sock,addr,dataCenter,configsDict))
    t.start()
    #sock.close()
s.close()

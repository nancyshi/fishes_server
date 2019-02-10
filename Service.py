import socket
import threading
from ipConfigMgr import ipConfigMgr

class Service(object):
    def __init__(self):
        self.socket = socket.socket()
        self.ip = ipConfigMgr["ip"]
        self.ports = ipConfigMgr["ports"]
        self.port = None
    def handller(self,sock,addr):
        pass
    def splitData(self,data):
        data = data.decode("utf-8")
        splitedData = data.split("\r\n\r\n")
        if len(splitedData) != 3:
            print("erro: received an invalid data ")
            return
        header, requestInfo, requestBody = splitedData

        splitedRequestInfo = requestInfo.split("\r\n")
        if len(splitedRequestInfo) != 2:
            print("erro: received an invalid requestInfo ")
            return
        requestType, playerId = splitedRequestInfo
        return (header,requestType,playerId,requestBody)

    def start(self):
        print("%s start to run at %s : %s" % (self.__class__.__name__, self.ip,self.port))
        self.socket.bind((self.ip,self.port))
        self.socket.listen()
        while True:
            sock,addr = self.socket.accept()
            #print("%s get a connection for %s" % (self.__class__.__name__, addr))
            t = threading.Thread(target=self.handller,args=(sock,addr))
            t.start()

    def stop(self):
        self.socket.close()
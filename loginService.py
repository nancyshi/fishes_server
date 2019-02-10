from Service import Service
import requestTypeEnum

class LoginService(Service):
    def __init__(self):
        super().__init__()
        self.port = self.ports["playerLoginService"]

    def handller(self, sock, addr):
        data = sock.recv(1024)
        header, requestType, token, requestBody = self.splitData(data)
        if requestType == requestTypeEnum.LoginReqType.login.value:
            
            userID = self.getUserIdByToken(token)
            backMessageHeader = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n"
            backMessage = backMessageHeader + str(userID)
            sock.send(bytes(backMessage,"utf-8"))

        sock.close()
    def getUserIdByToken(self,token):
        return 10001
    
loginService = LoginService()
from dataMgr import dataMgr
from playerDataService import playerDataService
from loginService import loginService
import threading

def startOneService(service):
    t = threading.Thread(target=service.start)
    t.start()

dataMgr.checkDBInfo()
startOneService(playerDataService)
startOneService(loginService)

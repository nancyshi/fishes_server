
from requestResponser import requestResponser
from dataMgr import dataMgr

dataMgr.checkDBInfo()
dataMgr.startAutoSaveDataToDB()
requestResponser.port = requestResponser.prots["playerLoginService"]
requestResponser.start()

from wsResponser import wsResponser
from dataMgr import dataMgr


dataMgr.checkDBInfo()
dataMgr.startAutoSaveDataToDB()
wsResponser.start()

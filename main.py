
from TornadoLoginService import tornadoLoginService
from dataMgr import dataMgr

dataMgr.checkDBInfo()
tornadoLoginService.port = tornadoLoginService.prots["playerLoginService"]
tornadoLoginService.start()
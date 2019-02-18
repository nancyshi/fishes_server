from TornadoService import TornadoService
import tornado.web
from dataMgr import dataMgr
from configMgr import configsDict
import tornado.escape

class BassHandler(tornado.web.RequestHandler):
    def get_json_argument(self, name, default = None):
        args = tornado.escape.json_decode(self.request.body)
        name = tornado.escape.to_unicode(name)
        if name in args:
            return args[name]
        elif default is not None:
            return default
        else:
            raise tornado.web.MissingArgumentError(name)

class MainHandller(BassHandler):
    def post(self):
        token = self.get_json_argument("token")
        playerId = self.getPlayerIdByToken(token)
        self.write(str(playerId))
        self.flush()
        self.finish()
        

    def getPlayerIdByToken(self,token):
        return 10001

class GetInitDataHandller(BassHandler):
    def post(self):
        playerId = self.get_json_argument("playerId")
        jsonData = dataMgr.queryInitData(playerId,configsDict)
        self.write(jsonData)
        self.set_header("Content-Type","text")
        self.flush()
        self.finish()
class UpdatePlayerDataHandller(BassHandler):
    def post(self):
        playerDatasForChange = self.get_json_argument("datasForChange")
        # print("playerDatasForChange is : %s" % playerDatasForChange)
        # dic = json.loads(playerDatasForChange)
        dataMgr.updatePlayerData(playerDatasForChange)

        self.write("success")
        self.flush()
        self.finish()



requestResponser = TornadoService([
    (r"/",MainHandller),
    (r"/getinitdata",GetInitDataHandller),
    (r"/updateplayerdata",UpdatePlayerDataHandller),
])
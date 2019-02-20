import tornado.ioloop
import tornado.web
from ipConfigMgr import ipConfigMgr

class TornadoService(tornado.web.Application):
    port = ipConfigMgr["port"]


    def start(self):
        self.listen(self.port,"0.0.0.0")
        print("%s now start at port : %s" %(self.__class__.__name__, self.port))
        tornado.ioloop.IOLoop.current().start()



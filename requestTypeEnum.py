from enum import Enum
class PlayerDataReqType(Enum):
    getInitData = "GID"
    updatePlayerData = "UPD"  

class LoginReqType(Enum):
    login = "LI"

class RequestTypeEnum(Enum):
    playerDataService = PlayerDataReqType
    loginService = LoginReqType

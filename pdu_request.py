import json


class PDURequest:
    __version = 1.0

    def __init__(self, command, parameters, channel, payload):
        self.version = PDURequest.__version
        self.command = command  # 4 char command text
        self.parameters = parameters  # list of parameters
        self.channel = channel  # AC | CC | DC
        self.payload = payload  # chat text

    def createRequestStr(self):
        str_req = json.dumps(self.__dict__)  # serialization
        str_req += "\n"  # termination character
        return str_req

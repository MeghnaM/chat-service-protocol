import json


class PDUResponse:
    __version = 1.0

    def __init__(self, code, parameters, channel, payload):
        self.version = PDUResponse.__version
        self.response_code = code
        self.parameters = parameters
        self.channel = channel
        self.payload = payload

    def createResponseStr(self):
        str_resp = json.dumps(self.__dict__)        # serialization
        str_resp += "\n"        # termination character
        return str_resp

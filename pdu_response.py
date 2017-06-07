import json


class PDUResponse:
    """Responses from server are made into the PDUResponse object"""

    __version = 1.0

    def __init__(self, code, parameters, channel, payload):
        self.version = PDUResponse.__version
        self.response_code = code                   # 3 digit response code | string
        self.parameters = parameters                # JSON obj of parameters
        self.channel = channel                      # AC | CC | DC
        self.payload = payload                      # Data

    def createResponseStr(self):
        """Serializes PDUResponse object"""
        str_resp = json.dumps(self.__dict__)        # serialization
        str_resp += "\n"                            # termination character
        return str_resp

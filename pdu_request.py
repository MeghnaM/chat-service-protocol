import json


class PDURequest:
    """Requests from client are made into the PDURequest object"""

    def __init__(self, version, command, parameters, channel, payload):
        self.version = version                  # client version
        self.command = command                  # 4 char command text
        self.parameters = parameters            # JSON object with parameters
        self.channel = channel                  # AC | CC | DC
        self.payload = payload                  # chat text | data

    def createRequestStr(self):
        """Serializes PDURequest object"""

        str_req = json.dumps(self.__dict__)     # serialization
        str_req += "\n"                         # termination character
        return str_req

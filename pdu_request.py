import json

"""Requests from client are made into the PDURequest object"""
class PDURequest:
    """Constructor for PDURequest"""
    def __init__(self, version, command, parameters, channel, payload):
        self.version = version                  # Client protocol version
        self.command = command                  # 4 char command text
        self.parameters = parameters            # JSON object with parameters
        self.channel = channel                  # AC | CC | DC
        self.payload = payload                  # chat text | data

    """Serializes PDURequest object"""
    def createRequestStr(self):
        str_req = json.dumps(self.__dict__)     # serializes object to string
        str_req += "\n"                         # appends the termination character
        return str_req

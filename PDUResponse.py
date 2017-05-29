class PDUResponse:
    __version = 1.0

    def __init__(self, code, parameters, channel, payload):
        self.version = PDUResponse.__version
        self.response_code = code
        self.parameters = parameters
        self.channel = channel
        self.payload = payload

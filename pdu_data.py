class PDUData:
    def __init__(self, nick="", params=[], channel="", payload=""):
        self.nick = nick                    # nickname of user
        self.message_parameters = params    # 512 byte parameter space
        self.channel_identifier = channel   # 3 bit channel identifier
        self.payload = payload              # null terminated ASCII payload

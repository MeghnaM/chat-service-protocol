



class PDUData:
    c = socket()
    def __init__(self):
    
     self.nick = ""  #nickname of user
     self.message_parameters = ""  # 512 byte parameter space
     self.channel_identifier = "" #3 bit channel identifier
     self.payload = "\0"                         #null terminated ASCII payload
   
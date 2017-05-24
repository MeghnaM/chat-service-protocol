from bitstring import BitArray
from logging.config import IDENTIFIER


class PDURequest:
    
    def __init__(self):
        
        self.message_identifier = BitArray(256) # 32 byte message idenfitier
        self.message_parameters = BitArray(4096)  # 512 byte parameter space
        self.channel_identifier = BitArray(3) #3 bit channel identifier
        self.pdu_size = BitArray(64)            #8 byte integer indicating size of PDU
        self.checksum = BitArray(64)            #8 byte checksum
        self.payload = "\0"                         #null terminated ASCII payload
     
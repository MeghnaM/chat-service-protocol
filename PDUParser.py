import PDURequest as req 
import PDUResponse as rep
from test import test_unicode_identifiers
from bitstring import BitArray
import request_handler
import response_handler



print("test HEllo")


#switch statement taken from https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python#comment39185309_60215



class PDUParser:
    #dsefine a simple state machine based on PDU input
        
        
    def parseRequestPDUS(self, pduRequest, pduData):
    
        #PDU data for Request
        message_identifier = BitArray(256) # 32 byte message idenfitier
        message_parameters = BitArray(4096)  # 512 byte parameter space
        channel_identifier = BitArray(3) #3 bit channel identifier
        pdu_size = BitArray(64)            #8 byte integer indicating size of PDU
        checksum = BitArray(64)            #8 byte checksum
        payload = "\0"                         #null terminated ASCII payload
        
        # STRIP data from incoming PDU
        
        message_identifier = pduRequest.message_identifier
        message_parameters = pduRequest.message_parameters
        channel_identifier = pduRequest.channel_identifier
        pdu_size = pduRequest.pdu_size
        checksum = pduRequest.checksum
        payload = pduRequest.payload
     
     #State Machine - parse message_identifier
        
        identifier = message_identifier.decode(encoding="utf-8")
        
        print("Requesting identifier: " % identifier)
        
        #PDU Data
        
        req_handler = RequestHandler()
        
        req_handler.pduData = pduData
        
        reqs_dict[identifier]
            
            
    
        
    def parseResponsePDUs(self, pduResponse, pduData):
        #PDU data for response
        message_identifier = BitArray(96) # 12 byte message idenfitier
        message_parameters = BitArray(4096)  # 512 byte parameter space
        channel_identifier = BitArray(3) #3 bit channel identifier
        pdu_size = BitArray(64)            #8 byte integer indicating size of PDU
        checksum = BitArray(64)            #8 byte checksum
        var = "\0"                         #null terminated ASCII payload
        
        #STRIP data from incoming PDU
    
        message_identifier = pduResponse.message_identifier
        message_parameters = pduResponse.message_parameters
        channel_identifier = pduRequest.channel_identifier
        pdu_size = pduResponse.pdu_size
        checksum = pduResponse.expectedchecksum
        payload = pduResponse.payload


        identifier = message_identifier.decode(encoding="utf-8")
        
        print("Requesting identifier: " % identifier)
        
        
        resp_handler = ResponseHandler()
        
        resp_handler.pduData = pduData
  
        resp_handler.resp_dict[identifier]
        
        


import PDURequest
import PDUResponse
from test import test_unicode_identifiers
from bitstring import BitArray

print("test HEllo")




class PDUStateMachine:
    #dsefine a simple state machine based on PDU input
        
        
    def parseRequestPDUS(self, pduRequest):
    
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
        checksum = pduRequest.expectedchecksum
        payload = pduRequest.payload
     
     #State Machine - parse message_identifier
     
        identifier = message_identifier.decode()
        print("Requesting identifier: " % identifier)
        
        for case in switch(identifier):
            if case('REDY'):
                readyAction()
                break
            if case('NICK'):
                nickAction()
                break
            if case('JOIN'):
                joinAction()
                break
            if case('PART'):
                partAction()
                break
            if case('MSSG'):
                mssgAction()
                break
                
            if case('KICK'):
                kickAction()
                break
            
            if case('BANK'):
                banAction()
                break
            if case('BLAK'):
                blackAction()
                break
            if case('ELVT'):
                elevateAction()
                break
            if case('DROP'):
                dropAction()
                break
            if case('LIST'):
                listAction()
                break
            if case('PMSG'):
                privateMessageAction()
                break
            if case('PRVM'):
                endPrivateMessageAction()
                break
            if case('PMSS'):
                sendPrivateMessageAction()
                break
            if case('MAIL'):
                mailAction()
                break
            if case('QUIT;'):
                quitAction()
                break
            if case('KEEP'):
                keepAliveAction()
                break
            
            
            
            
            
            
            #MNICK, CHAT, JOIN
                
            
            
    
        
    def parseResponsePDUs(self, pduResponse):
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
        
        identifier = message_identifier.decode()
        print("Sending Response" % identifier)
        
        #State Machine - parse message_identifier
     
        identifier = message_identifier.decode()
        print("Requesting identifier: " % identifier)
       
        for case in switch(identifier):
            if case('100'):
                acknowledgeConnectionAction()
                break
            if case('110'):
                authenticationSuccessfulAction()
                break
            if case('200'):
                authenticationFailedAction()
                break
            if case('210'):
                serverDoesNotAcknowledgeAction()
                break
            if case('120'):
                receivingMessageAction()
                break
            if case('160'):
                receivePrivateChatMessageAction()
                break
            if case('130'):
                receiveListOfChannelsAction()
                break
            if case('140'):
                receiveQueuedMessagesAction()
                break
            if case('150'):
                receivePositiveAcknowledgmentAction()
                break
            if case('210'):
                receiveNegativeAcknowledgementAction()
                break
            if case('300'):
                receiveGeneralErrorCodeAction()
                break
            if case('310'):
                receiveUnknownCommandErrorAction()
                break
            if case('320'):
                recieveSyntaxErrorAction()
                break
       
test1 = PDUStateMachine()

PDUREQ = PDURequest()

test1.parseRequestPDUS(PDUREQ)



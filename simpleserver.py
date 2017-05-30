#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
PDUParser = parser()
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ("Got connection from', addr")
   c.send('Thank you for connecting')
   #c.close()                # Close the connection
   #create receive buffer
   receive_buffer = string()
   #process any data received
   #pass off as PDU to PDUProcessor
   in_data = c.recv(receive_buffer)
   pduData = PDUData()
   pduData.c = c
   
   #in data should be a PDURequest object
   #parses and executes a PDU action
   if in_data != "":     
       parser.parseRequestPDU(in_data, pduData)

    
   
   


#data structures for server


chatrooms = []
user_profiles =  []


#data structure implementation

def joinchat(pduData):
    
    chatrooms[PDUData.channel_identifier].users.append(user.nickname)
    user_profiles[PDUData.nickname].channels_attending.append(PDUData.channel_identifier)
    
    #build a PDU to send back
    
    responsePDU = PDUResponse()
    
    #self.version = PDUResponse.__version
    #self.response_code = code
    #self.parameters = parameters
    #    self.channel = channel
     #   self.payload = payload
    
    #PUT A VERSION CONSTANT SOMEWHERE
    responsePDU.version = 2
    #send `150 - generic positive acknowledgment
    responsePDU.response_code = 150
    pduData.c.sendall(responsePDU)
    #return PDU acknowledgement code 150 - positive acknowledgement
    
def partchat(pduData):
    chatrooms[PDUData.channel_identifier].users.remove(user.nickname)
    user_profiles[PDUData.nickname].attending.remove(PDUData.channel_identiftier)
    #return PDU acknowledgment code 150 positive acknowledgement
    #build a PDU to send back
    
    responsePDU = PDUResponse()
    
    #self.version = PDUResponse.__version
    #self.response_code = code
    #self.parameters = parameters
    #    self.channel = channel
     #   self.payload = payload
    
    #PUT A VERSION CONSTANT SOMEWHERE
    responsePDU.version = 2
    #send `150 - generic positive acknowledgment
    responsePDU.response_code = 150
    pduData.c.sendall(responsePDU)
    #return PDU acknowledgement code 150 - positive acknowledgement
    
    
def messagechat(pduData):
    #broadcast message to all chatroom clients
    #foreach user in the chatroom class
    #return the message PDU to their client
    chatrooms[PDUData.channel_identifier].contents.append(PDUData.payload)
    for u in chatrooms[PDUData.channel_identifier].users:
        #build a PDU to send back
    
        responsePDU = PDUResponse()
        responsePDU.version = 2
        responsePDU.response_code = 120
        #nick, channel, and ascii text
        responsePDU.parameters = pduData.parameters
        responsePDU.channel = PDUData.channel_identifier
        responsePDU.payload = pduData.payload
        
        #how do we send all to multiple users in a group chat
        pduData.c.sendall(responsePDU)
        #self.version = PDUResponse.__version
    #self.response_code = code
    #self.parameters = parameters
    #    self.channel = channel
     #   self.payload = payload
    
    #PUT A VERSION CONSTANT SOMEWHERE
    responsePDU.version = 2
    #send `150 - generic positive acknowledgment
    responsePDU.response_code = 150
    pduData.c.sendall(responsePDU)
    #return PDU acknowledgement code 150 - positive acknowledgement
            
        #return 120 to client, nick, chatname, and ascii text
        

def elevatechat(pduData):
    
    #elevate user in chatroom
    chatrooms[PDUData.channel_identifier].elevated_users(user.nickname)
    
def quitchat(pduData):
    #disconnect from client
    pass
    
def dropchat(pduData):
    #drop user privelages in chat
    chatrooms[PUData.channel_identifier].elevated_users.remove(user.nickname)
    
def mailchat(pduData):
    pass
    #return queued  mail to client
    #return code 140 and ASCII text

def kickchat(pduData):
    
    #server removces a user from a chatname
    chatroooms[PDUData.channel_identifier].users.remove(user.nickname)

def banchat(pduData):
    #server kicks the user and bans them temporarily
    chatrooms[PDUData.channel_identifier].users.remove(user.nickname)
    chatrooms[PDUData.channel_identifier].banned_users.append(user.nickname)
    
def blackchat(pduData):
    #server blacklists user
    chatroooms[PDUData.channel_identifier].users.remove(user.nickname)
    chatrooms[PDUData.channel_identifier].black_users.append(user.nickname)
    
def privatechat(pduData):
    pass

    
    
    
    
    
    
    
    
    
    
    
    
    
    
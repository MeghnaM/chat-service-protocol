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
   if in_data != "":     
       parser.parseRequestPDU(in_data, pduData, c)

    
   
   


#data structures for server


chatrooms = []
user_profiles =  []


#data structure implementation

def joinchat(PDUData):
    
    chatrooms[PDUData.channel_identifier].users.append(user.nickname)
    user_profiles[PDUData.nickname].channels_attending.append(PDUData.channel_identifier)
    #return PDU acknowledgement code 150 - positive acknowledgement
    
def partchat(PDUData):
    chatrooms[PDUData.channel_identifier].users.remove(user.nickname)
    user_profiles[PDUData.nickname].attending.remove(PDUData.channel_identiftier)
    #return PDU acknowledgment code 150 positive acknowledgement
    
def messagechat(PDUData):
    #broadcast message to all chatroom clients
    #foreach user in the chatroom class
    #return the message PDU to their client
    chatrooms[PDUData.channel_identifier].contents.append(PDUData.payload)
    for u in chatrooms[PDUData.channel_identifier].users:
        #send a message to the client to refresh
        
        #return 120 to client, nick, chatname, and ascii text
        pass

def elevatechat(PDUData):
    
    #elevate user in chatroom
    chatrooms[PDUData.channel_identifier].elevated_users(user.nickname)
    
def quitchat(PDUData):
    #disconnect from client
    pass
    
def dropchat(PDUData):
    #drop user privelages in chat
    chatrooms[PUData.channel_identifier].elevated_users.remove(user.nickname)
    
def mailchat(PDUData):
    pass
    #return queued  mail to client
    #return code 140 and ASCII text

def kickchat(PDUData):
    
    #server removces a user from a chatname
    chatroooms[PDUData.channel_identifier].users.remove(user.nickname)

def banchat(PDUData):
    #server kicks the user and bans them temporarily
    chatrooms[PDUData.channel_identifier].users.remove(user.nickname)
    chatrooms[PDUData.channel_identifier].banned_users.append(user.nickname)
    
def blackchat(PDUData):
    #server blacklists user
    chatroooms[PDUData.channel_identifier].users.remove(user.nickname)
    chatrooms[PDUData.channel_identifier].black_users.append(user.nickname)
    
def privatechat(PDUData):
    pass

    
    
    
    
    
    
    
    
    
    
    
    
    
    
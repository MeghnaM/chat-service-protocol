#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ("Got connection from', addr")
   c.send('Thank you for connecting')
   c.close()                # Close the connection
   
   


#data structures for server


chatroom = chat_room()
user_profile = user()


#data structure implementation

def joinchat(PDUData):
    
    chatroom.users.append(user.nickname)
    user_profile.channels_attending.append(PDUData.channel_identifier)
    #return PDU acknowledgement code 150 - positive acknowledgement
    
def partchat(PDUData):
    chatroom.users.remove(user.nickname)
    user_profile.channels_attending.remove(PDUData.channel_identiftier)
    #return PDU acknowledgment code 150 positive acknowledgement
    
def messagechat(PDUData):
    #broadcast message to all chatroom clients
    #foreach user in the chatroom class
    #return the message PDU to their client
    chatroom.contents.append(PDUData.payload)
    for u in chatroom.users:
        #send a message to the client to refresh
        
        #return 120 to client, nick, chatname, and ascii text
        pass

def elevatechat(PDUData):
    
    #elevate user in chatroom
    chatroom.elevated_users(user.nickname)
    
def quitchat(PDUData):
    #disconnect from client
    pass
    
def dropchat(PDUData):
    #drop user privelages in chat
    chatroom.elevated_users.remove(user.nickname)
    
def mailchat(PDUData):
    pass
    #return queued  mail to client
    #return code 140 and ASCII text

def kickchat(PDUData):
    
    #server removces a user from a chatname
    chatrooom.users.remove(user.nickname)

def banchat(PDUData):
    #server kicks the user and bans them temporarily
    chatroom.users.remove(user.nickname)
    chatroom.banned_users.append(user.nickname)
    
def blackchat(PDUData):
    #server blacklists user
    chatrooom.users.remove(user.nickname)
    chatroom.black_users.append(user.nickname)
    
def privatechat(PDUData):
    pass

    
    
    
    
    
    
    
    
    
    
    
    
    
    
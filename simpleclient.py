#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ("Got connection from", addr)
   c.send('Thank you for connecting')
   c.close()                # Close the connection
   


#client receive functions

client_user = user()
chat_rooms = []

def updateChatWindow():
    for ch in chat_rooms:
        for txt in ch:
            print(txt.chat_contents)
    


def joinclient(PDUData):
    chat_rooms.append(PDUData.channel_identifier)
    client_user.channels_attending.append(PDU.channel_identifier)
    
def partclient(PDUData):
    chat_rooms.remove(PDUData.channel_identifier)
    client_user.channels_attending.remove()
    

    

    
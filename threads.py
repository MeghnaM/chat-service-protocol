#!/usr/bin/env python

import threading
import time
import client

# Subclass of the Thread class, that implements a new thread using the threading module
class myThread (threading.Thread):
   threadLock = threading.Lock()

   # Override of the __init__ method to add additional arguments
   def __init__(self, threadId, name, channel):
      threading.Thread.__init__(self)  # Calling the constructor of its parent
      self.threadId = threadId
      self.name = name
      self.channel = channel

   # Override of the run() method to implement what the thread should do when started
   def run(self):
      print( "Starting " + self.name + "...")
      myThread.threadLock.acquire()       # Get lock to synchronize threads
      self.channel.connect()              # Establish connection between the client and the server
      
      #read input from channel and respond accordingly
      #for example, if received NICK call function to authenticate
      #if received JOIN call function to join chat
      # use dict
      
      myThread.threadLock.release()       # Free lock to release next thread

# TODO: Exception Handling
class Threads:

   def __init__(self, controlPort, dataPort, adminPort):
      self.controlChannel = client.Client(controlPort)
      self.dataChannel = client.Client(dataPort)
      #self.adminChannel = client.Client(adminPort)

   # Initiate connection from the client to the server
   def initiateConnection(self):
      print ("Connecting to the control channel on the server...")
      self.controlChannel.connect()

   # Create and start additional threads
   def spawnThreads(self):
      dataThread = myThread(1, "Data Thread", self.dataChannel)
      dataThread.start()

   # TODO: Be able to send messages over each thread separately

   def closeConnection(self):
      self.controlChannel.closeConnection()
      print ("Connection to the control channel has been closed successfully!")

if __name__ == '__main__':
   controlPort = 11111
   dataPort = 11112
   adminPort = 11113
   mainThread = Threads(controlPort, dataPort, adminPort)
   mainThread.initiateConnection()
   mainThread.spawnThreads()
   #mainThread.closeConnection()



parse_rcv_dict = {
    "REDY": readyServer(),
    "NICK": authenticateUser(),
    "JOIN": joinUser(nick, chatname),
    #"PART": partAction(),
    "MSSG": mssgUser(nick, chatname, asciitext),
    "KICK": kickUser(),
    "BANK": banUser(nick, chatname),
    "BLAK": blackUser(nick, chatname),
    #"ELVT": elevateUser(nick, chatname)
    #"DROP": dropAction(),
    "LIST": listUser(self, nick),
    #"PMSG": privateMessageAction(),
    #"PRVM": endPrivateMessageAction(),
    #"PMSS": sendPrivateMessageAction(),
    #"MAIL": mailAction(),
    "QUIT": quitAction()
    #"KEEP": keepAliveAction()
}

#chatrooms currently open in the client

open_chats = []


def readyServer():
    #client requests connection to server (PDU REDY) through control channel (in)
    #Server responds with (PDU 100 if successful) through control channel (out)
    pass

def authenticateUser(self, nick, password):
    #get user name and password from the control channel (from the PDU sent) (in)
    #authenticate
    #create PDU 110 if successsful and pass to the control channel (out)
    #send PDU to control channel
    pass

def joinUser(self, nick, chatname):
    #get a JOIN PDU (in) through control chanel (in)
    #server responds by calling a join chat function
    #server responds by adding CHATNAME to the list of open chats
    pass

def mssgUser(self, nick, chatname, asciitext):
    #get a MSSG PDU (in) throught he data channel
    #server responds by adding the ascii text to the chat room object
    pass
  
def kickUser(self, nick, chatname):  
    #receive a KICK PDU (in) through the control channel
    #server responds by re3moving the user from the chat_room object
    pass

def banUser(self, nick, chatname):
     #receive a BAN PDU (in) tghrough the control channenl
     #server responds by removing the user from the chat_room object
     #server responds by adding the user to the chat_room object's ban list
     pass
 
def blackUser(self, nick, chatname):
    #recieve a BLAK PDU (in) through the control channel
    #serve rresponds by removing the user from the chat_room_object
    #server responds by adding the user to the chat_rooom's black list'
    pass

def listUser(self, nick):
    #receive a LIST PDU (in) through the control channel
    #server responds by PDU 130 and a list of ascii text
    #client displays ascii text
    pass

def quitAction(self, nick):
    #receive a QUIT message throguh the control channel (in)
    #server disconnects
    pass


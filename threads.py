#!/usr/bin/env python

import threading
import time
import client

# Subclass of the Thread class, that implements a new thread using the threading module
class myThread (threading.Thread):

   # Override of the __init__ method to add additional arguments
   def __init__(self, threadId, name):
      threading.Thread.__init__(self)  # Calling the constructor of its parent
      self.threadId = threadId
      self.name = name

   # Override of the run() method to implement what the thread should do when started
   def run(self):
      print "Starting " + self.name
      print "Running thread: " + self.name
      print "Exiting " + self.name

# TODO: Exception Handling
class Threads:

   def __init__(self, controlPort, dataPort, adminPort):
      self.controlChannel = client.Client(controlPort)
      #self.dataChannel = client.Client(dataPort)
      #self.adminChannel = client.Client(adminPort)

   # Initiate connection from the client to the server
   def initiateConnection(self):
      print "Connecting to the control channel on the server..."
      self.controlChannel.connect()

   # Spawn threads
   def createAndStartThreads(self):
      dataThread = myThread(1, "Data Thread")
      dataThread.start()

   # Be able to send messages over each thread separately

   def closeConnection(self):
      self.controlChannel.closeConnection()
      print "Connection to the control channel has been closed successfully!"

if __name__ == '__main__':
   controlPort = 11112
   dataPort = 222
   adminPort = 333
   mainThread = Threads(controlPort, dataPort, adminPort)
   mainThread.initiateConnection()
   #thread.createAndStartThreads()
   mainThread.closeConnection()


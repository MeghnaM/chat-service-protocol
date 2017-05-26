#!/usr/bin/python

import socket

class Client:
   socket = socket.socket()         # Create a socket object
   host = "127.0.0.1"               # IP address of my local network

   def __init__(self, port):
      self.port = port

   def connect(self):
      host = Client.host
      socket = Client.socket
      socket.connect((host, self.port))
      print(socket.recv(1024))

   def closeConnection(self):
      socket.close                     # Close the socket when done
      print "The connection to port", self.port, "has been closed"

if __name__ == '__main__':
   port = 111
   cl = Client(port)
   cl.connect()
   cl.closeConnection()

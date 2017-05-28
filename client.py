#!/usr/bin/python
import socket

class Client:
   host = "127.0.0.1"                  # IP address of my local network

   def __init__(self, port):
      self.port = port
      self.socket = socket.socket()    # Create a new socket object

   def connect(self):
      host = Client.host
      self.socket.connect((host, self.port))
      print(self.socket.recv(1024))

   def closeConnection(self):
      self.socket.close                # Close the socket when done
      print ("The connection to port", self.port, "has been closed")

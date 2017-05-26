#!/usr/bin/python
import socket

class Server:
   socket = socket.socket()            # Create a socket object
   host = "127.0.0.1"                  # IP address of my local network

   def __init__(self, port):
      self.port = port

   def connect(self):
      host = Server.host
      socket = Server.socket
      socket.bind((host, self.port))   # Bind to the port
      socket.listen(5)                 # Now wait for client connection

      while True:
         connObj, addr = socket.accept()     # Establish connection with client, and returns a connection object which represents that connection
         print ("Got connection from", addr)
         connObj.send('Server to Client: Thank you for connecting, now this connection will be closed.')
         connObj.close()

if __name__ == '__main__':
   port = 11112
   server = Server(port)               # Start a server which listens on the given port
   server.connect()

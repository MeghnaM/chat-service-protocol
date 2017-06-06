#!/usr/bin/python
import socket
import sys
import threading

BUFSIZE = 1024

class Server:
   HOST = "127.0.0.1"                  # IP address of my local network

   def __init__(self, port, backlog=5):
      self.PORT = port
      # Create an INET, STREAMing socket
      serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print 'Socket created'

      # Bind socket to local host and port
      # Binding to local host means that this socket is only visible within this machine
      try:
         serversocket.bind((HOST, self.PORT))
      except socket.error as msg:
         print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
         sys.exit()
      print 'Socket bind complete'

      # Become a server socket by listening on socket
      serversocket.listen(5)
      print 'Socket now listening'

   # Function for handling connections, also used to create threads
   def clientthread(conn):
      # Sending message to connected client
      conn.send('Welcome to the server. Type something and hit enter\n') # send only takes strings

      # Infinite loop so that the function does not terminate and the thread does not end
      while True:
         # Receiving from client
          data = conn.recv(1024)
          reply = 'OK...' + data
          if not data:
             break
         conn.sendall(reply)

      # Came out of loop
      conn.close()

      # Now, keep talking with the client
      while 1:
         # Wait to accept a connection - blocking call
         conn, addr = s.accept()
         print 'Connected with ' + addr[0] + ':' + str(addr[1])

         # Start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
         controlThread = threading.Thread(name='control', target=clientthread, args=(conn,))
         #threading.start_new_thread(clientthread ,(conn,))

      s.close()

#   def connect(self):
#      host = Server.host
#      socket = Server.socket
#      socket.bind((host, self.port))   # Bind to the port
#      socket.listen(5)                 # Now wait for client connection

#      while True:
#         connObj, addr = socket.accept()     # Establish connection with client, and returns a connection object which represents that connection
#         print ("Got connection from", addr)
#         connObj.send('Server to Client: Thank you for connecting') #, now this connection will be closed.')
         #connObj.close()

#if __name__ == '__main__':
#   controlPort = 11111
#   dataPort = 11112
#   controlChannel = Server(controlPort)      # Initialize the server channel with a given port
#   dataChannel = Server(dataPort)
#   controlChannel.connect()                  # Connect to the channel on the server
#   dataChannel.connect()

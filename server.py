#!/usr/bin/python
import socket
import sys
import signal
import select
from communication import send, receive

BUFSIZE = 1024

class Server:
   host = "127.0.0.1"                  # IP address of my local network

   def __init__(self, port, backlog=5):
      self.port = port
      self.clients = 0
      self.clientMap = {}
      self.outputs = []
      self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.server.bind((host, port))
      print 'Listening on port', port, '...'
      self.server.listen(backlog)
      # Trap keyboard interrupts
      signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        # Close the server
        print 'Shutting down server...'
        # Close existing client sockets
        for o in self.outputs:
            o.close()
        self.server.close()

    def getname(self, client):
        # Return the printable name of the
        # client, given its socket...
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def serve(self):
        inputs = [self.server,sys.stdin]
        self.outputs = []
        running = 1
        while running:
            try:
                inputready,outputready,exceptready = select.select(inputs, self.outputs, [])
            except select.error, e:
                break
            except socket.error, e:
                break
            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print 'chatserver: got connection %d from %s' % (client.fileno(), address)
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]
                    # Compute client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)
                    # Send joining information to other clients
                    msg = '\n(Connected: New client (%d) from %s)' % (self.clients, self.getname(client))
                    for o in self.outputs:
                        # o.send(msg)
                        send(o, msg)
                    self.outputs.append(client)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    # handle all other sockets
                    try:
                        # data = s.recv(BUFSIZ)
                        data = receive(s)
                        if data:
                            # Send as new client's message...
                            msg = '\n#[' + self.getname(s) + ']>> ' + data
                            # Send data to all except ourselves
                            for o in self.outputs:
                                if o != s:
                                    # o.send(msg)
                                    send(o, msg)
                        else:
                            print 'chatserver: %d hung up' % s.fileno()
                            self.clients -= 1
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                            # Send client leaving information to others
                            msg = '\n(Hung up: Client from %s)' % self.getname(s)
                            for o in self.outputs:
                                # o.send(msg)
                                send(o, msg)
                    except socket.error, e:
                        # Remove
                        inputs.remove(s)
                        self.outputs.remove(s)
        self.server.close()

if __name__ == "__main__":
    Server.serve()

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

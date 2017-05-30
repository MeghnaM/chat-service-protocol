import asynchat
import asyncore
import socket
import threading
import sys

class ChatClientA(asynchat.async_chat):

    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.set_terminator('\n')
        self.buffer = []

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        msg = ''.join(self.buffer)
        print 'Client A received:', msg
        self.buffer = []

    def handle_close(self):
        self.close()
        print "Client A's connection has been terminated"
        #comm.daemon = False

client = ChatClientA('localhost', 12345)

comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()

while True:
    msg = raw_input('ClientA: ')
    client.push(msg + '\n')
    if msg == "logout":
      client.handle_close()
      break

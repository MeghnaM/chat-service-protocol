import asynchat
import asyncore
import socket
import threading
import sys

class ChatClient(asynchat.async_chat):

    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.set_terminator('\n')
        self.buffer = []

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        pass

    def handle_close(self):
        self.close()
        print "Client connection has been terminated"
        return

client = ChatClient('localhost', 5050)

comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()

while True:
    msg = raw_input('> ')
    client.push(msg + '\n')
    if msg == "logout":
      client.handle_close()
      break

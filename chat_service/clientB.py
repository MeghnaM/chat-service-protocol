import asynchat
import asyncore
import socket

class ChatClientB(asynchat.async_chat):

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
        print 'Client B received:', msg
        self.buffer = []

    def handle_close(self):
       self.close()
       print "Client B's connection has been terminated"
       return

client = ChatClientB('localhost', 12345)

print 'Listening on localhost:5050'
asyncore.loop()

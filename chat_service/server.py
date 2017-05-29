import asynchat
import asyncore
import socket
import sys

chat_room = {}

class ChatHandler(asynchat.async_chat):
    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
        self.set_terminator('\n')
        self.buffer = []

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        msg = ''.join(self.buffer)
        print 'Server received:', msg
        for handler in chat_room.itervalues():
            if hasattr(handler, 'push'):
                handler.push(msg + '\n')
        self.buffer = []
        # TODO: Update close condition - only when *all* the clients have logged out,
        #       should the server connection be terminated
        if msg == "logout":
           self.handle_close()

    def handle_close(self):
       self.close()
       print "Server session has been terminated"
       sys.exit(0)

class ChatServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock)

server = ChatServer('localhost', 12345)

print 'Serving on localhost:12345'
asyncore.loop(map=chat_room)

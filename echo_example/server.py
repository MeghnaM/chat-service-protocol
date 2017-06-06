import asyncore
import logging
import socket

from handler import Handler

class Server(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        #self.address = self.socket.getsockname()
        self.listen(5)
        return

    def serve(self):
       asyncore.loop(map=chat_room)

    def handle_accept(self):
        # Called when a client connects to our socket
        connection_socket, client_address = self.accept()
        Handler(sock=connection_socket)
        # We only want to deal with one client at a time,
        # so close as soon as we set up the handler.
        # Normally you would not do this and the server
        # would run forever or until it received instructions
        # to stop.
        #self.handle_close()
        #return

    def handle_close(self):
        self.close()

Server.serve()

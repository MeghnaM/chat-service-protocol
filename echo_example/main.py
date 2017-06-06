import asyncore
import logging
import socket

from server import Server
from client import Client

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

address = ('localhost', 0) # let the kernel give us a port
server = Server(address)
ip, port = server.address # find out what port we were given

message_data = open('sample.txt', 'r').read()
client = Client(ip, port, message=message_data)

asyncore.loop()

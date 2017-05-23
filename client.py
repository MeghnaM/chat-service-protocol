#!/usr/bin/python

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "127.0.0.1"          # IP address of my local network
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
s.close                     # Close the socket when done

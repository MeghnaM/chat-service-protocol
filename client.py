#!/usr/bin/python
import socket
import json
import PDURequest
import response_handler as resh

class Client:
    # IP address of my local network
    host = "127.0.0.1"

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket()       # Create a new socket object

    def connect(self):
        host = Client.host
        self.socket.connect((host, self.port))
        self.sendPDURequest()
        resp_obj = json.loads(self.socket.recv(1024).decode("utf-8"))       # byte-decoding and deserialization
        self.processResponse(resp_obj)

    def sendPDURequest(self):
        req = PDURequest.PDURequest("REDY", [], "CC", "Ready?")
        str_req_byte = bytes(json.dumps(req.__dict__), "utf-8")             # serializing and byte-encoding requestPDU
        self.socket.send(str_req_byte)

    def processResponse(self, resp_obj):
        resp_code = resp_obj["response_code"]
        resh_obj = resh.ResponseHandler()
        dict_val = resh_obj.resp_dict[resp_code]

    def closeConnection(self):
        self.socket.close()                 # Close the socket when done
        print("The connection to port", self.port, "has been closed")

client = Client(1234)
client.connect()
client.closeConnection()

#!/usr/bin/python
import socket
import json
import PDUResponse
import request_handler as reqh


class Server:
    # IP address of my local network
    host = "127.0.0.1"

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket()       # Create a new socket object

    def listen(self):
        host = Server.host
        self.socket.bind((host, self.port))
        self.socket.listen(5)

        while True:
            conn, addr = self.socket.accept()
            print("Got connection from", addr)
            req_obj = json.loads(conn.recv(1024).decode("utf-8"))           # byte-decoding and deserialization
            resp_code = self.processRequest(req_obj)
            self.createResponse(conn, resp_code)
            # self.closeConnection(conn)

    def processRequest(self, req_obj):
        command = req_obj["command"]

        # TODO: Validate command i.e. check if command exists and if command is valid for current state

        reqh_obj = reqh.RequestHandler()
        return reqh_obj.reqs_dict[command]

    def createResponse(self, conn, resp_code):
        resp_obj = PDUResponse.PDUResponse(resp_code, [], "CC", "Ready!")
        str_resp_byte = bytes(json.dumps(resp_obj.__dict__), "utf-8")       # serializing and byte-encoding requestPDU
        conn.send(str_resp_byte)

    def closeConnection(self, conn):
        conn.close()        # Close the socket when done
        print("The connection to port", self.port, "has been closed")

server = Server(1234)
server.listen()

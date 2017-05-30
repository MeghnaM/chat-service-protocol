import asynchat
import asyncore
import socket
import threading
import json
import os
import PDURequest
import response_handler as resh
import PDUData

class ChatClient(asynchat.async_chat):
    __host = "127.0.0.1"
    __port = 12345

    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\n')
        self.buffer = []

    def connect_to_server(self):
        self.connect((ChatClient.__host, ChatClient.__port))
        # self.sendPDURequest("REDY", [], "CC", "Ready?")

    def sendPDURequest(self, command, parameters, channel, payload):
        req = PDURequest.PDURequest(command, parameters, channel, payload)
        str_send = json.dumps(req.__dict__) + "\n"      # serializing
        self.push(str_send)

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        resp_str = ''.join(self.buffer)
        self.buffer = []

        resp_obj = json.loads(resp_str)         # deserialization
        self.processResponse(resp_obj)

    def processResponse(self, resp_obj):
        resp_code = resp_obj["response_code"]
        pdu_data_obj = PDUData.PDUData()
        pdu_data_obj.payload = resp_obj["payload"]

        resh_obj = resh.ResponseHandler(pdu_data_obj)
        resh_obj.resp_dict[resp_code]

    def handle_close(self):
        self.close()
        print "Client A's connection has been terminated"

client = ChatClient()
client.connect_to_server()

comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()

while True:
    msg = raw_input('-> ')
    filename = os.path.basename(__file__)
    msg = "(" + filename + ")" + msg
    client.sendPDURequest("MSSG", [], "DC", msg)

    if msg == "logout":
        client.handle_close()
        break

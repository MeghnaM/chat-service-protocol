import asynchat
import asyncore
import socket
import threading
import json
import os
import PDURequest
import response_handler as resh
import PDUData
import user


class ChatClient(asynchat.async_chat):
    __host = "127.0.0.1"
    __port = 12345

    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\n')
        self.buffer = []
        self.obj = {}
        self.authentication_complete = False

    def connect_to_server(self):
        self.connect((ChatClient.__host, ChatClient.__port))
        # self.sendPDURequest("REDY", {}, "CC", "Ready?")

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

        if resp_obj["response_code"] == "110":
            self.authentication_complete = True
            self.obj["authenticated"] = True
        elif resp_obj["response_code"] == "200":
            self.authentication_complete = True
            self.obj["authenticated"] = False
        else:
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

    # def handle_read(self):        # works when handler (on servers found_terminator) is set correctly
    #     resp_obj = json.loads(self.recv(1024))
    #     if resp_obj["response_code"] == "110":
    #         self.authentication_complete = True
    #         self.obj["authenticated"] = True
    #     elif resp_obj["response_code"] == "200":
    #         self.authentication_complete = True
    #         self.obj["authenticated"] = False

    def initiateDialog(self):
        print "Welcome to our CSP system. To continue, select one of the following"

        while True:
            print "1 -> Login"
            print "2 -> Sign up"
            user_input = raw_input("-> ")

            if user_input.__eq__("1"):
                username = raw_input("username-> ")
                password = raw_input("password-> ")
                creds = {"username": username, "password": password}
                self.sendPDURequest("AUTH", creds, "CC", "text")

                while not self.authentication_complete:
                    pass

                if self.obj["authenticated"]:
                    print("Login successful")
                    break
                else:
                    print "Either your username or password is incorrect"
                    self.obj = {}
                    continue

            elif user_input.__eq__("2"):
                username = raw_input("choose username-> ")
                password = raw_input("choose password-> ")

                self.createNewUser(username, password, {}, filename)
                print "Account created"
                break
            else:
                print "Invalid input, try again."

client = ChatClient()
client.connect_to_server()

comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()

# >>> NOTE: Write all request | response related commands after this!  <<<

client.initiateDialog()

while True:
    msg = raw_input('-> ')

    if msg == "logout":
        client.handle_close()
        break

    filename = os.path.basename(__file__)
    msg = "(" + filename + ")" + msg
    client.sendPDURequest("MSSG", {}, "DC", msg)
    # client.sendPDURequest("AUTH", [], "CC", "text")



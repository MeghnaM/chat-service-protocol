import asynchat
import asyncore
import socket
import threading
import json
import os
from pdu_request import PDURequest
from response_handler import ResponseHandler
import pdu_data

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
        self.create_group_resp_recv = False
        self.groupNames_received = False
        self.username = ""
        self.chat_name = ""
        self.isAdmin = True     # for testing
        self.groupNames = []
        self.movedOut = False

    def connect_to_server(self):
        self.connect((ChatClient.__host, ChatClient.__port))

    def sendPDURequest(self, command, parameters, channel, payload):
        str_send = PDURequest(command, parameters, channel, payload).createRequestStr()
        self.push(str_send)

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        resp_str = ''.join(self.buffer)
        self.buffer = []

        resp_obj = json.loads(resp_str)                                     # deserialization

        if resp_obj["response_code"] == "190":
            self.processResponse(resp_obj)
            self.movedOut = True

        elif resp_obj["response_code"] == "130":
            if self.username == resp_obj["parameters"]["username"]:
                self.groupNames = resp_obj["payload"]

                self.processResponse(resp_obj)

                self.obj["group_fetch_success"] = True
                self.groupNames_received = True
            else:
                return

        elif resp_obj["response_code"] == "240":
            if self.username == resp_obj["parameters"]["username"]:
                self.processResponse(resp_obj)

                self.obj["group_fetch_success"] = False
                self.groupNames_received = True
            else:
                return

        elif resp_obj["response_code"] == "180":
            if self.username == resp_obj["parameters"]["username"]:
                self.chat_name = resp_obj["parameters"]["chat_name"]
                self.processResponse(resp_obj)
            else:
                return

        elif resp_obj["response_code"] == "140":
            chat = resp_obj["payload"]

            if self.username == chat[1: len(self.username) + 1]:       # don't print on senders console
                return
            else:
                self.processResponse(resp_obj)
                print("-> "),           # comma added to allow next print to be on the same line
            pass

        elif resp_obj["response_code"] == "110":
            self.obj["authenticated"] = True
            self.authentication_complete = True

        elif resp_obj["response_code"] == "200":
            self.obj["authenticated"] = False
            self.authentication_complete = True

        elif resp_obj["response_code"] == "170":
            self.obj["groupCreated"] = True
            self.create_group_resp_recv = True

        elif resp_obj["response_code"] == "230":
            self.obj["groupCreated"] = False
            self.create_group_resp_recv = True

        else:
            self.processResponse(resp_obj)

    def processResponse(self, resp_obj):
        resp_code = resp_obj["response_code"]
        pdu_data_obj = pdu_data.PDUData()
        pdu_data_obj.payload = resp_obj["payload"]

        resh_obj = ResponseHandler(pdu_data_obj)
        return resh_obj.runResponseCodeAction(resp_code)

    def handle_close(self):
        self.close()
        print "Your connection has been terminated"

    def initiateDialog(self):
        print "Welcome to our CSP system. To continue, select one of the following"

        while True:

            print "1 -> Login"
            print "2 -> Sign up"
            user_input = raw_input("-> ")

            if user_input == "1":
                self.authentication_complete = False
                username = raw_input("username-> ")
                password = raw_input("password-> ")
                creds = {"username": username, "password": password, "chat_name": ""}
                self.sendPDURequest("AUTH", creds, "CC", "")

                while not self.authentication_complete:         # waits for server response
                    pass

                if self.obj["authenticated"]:
                    self.username = username
                    print("Login successful")
                    self.createChatGroups()
                    break
                else:
                    print "Either your username or password is incorrect"
                    continue

            elif user_input == "2":
                self.authentication_complete = False
                username = raw_input("choose username-> ")
                password = raw_input("choose password-> ")
                creds = {"username": username, "password": password, "chat_name": ""}
                self.sendPDURequest("NWUA", creds, "CC", "")

                while not self.authentication_complete:         # waits for server response
                    pass

                if self.obj["authenticated"]:
                    self.username = username
                    print("Account created")
                    self.createChatGroups()
                    break
                else:
                    print "Username already exists"
                    continue
            else:
                print "Invalid input, try again."
                continue

    def createChatGroups(self):
        while True:
            print "1 -> Join available groups"
            print "2 -> Create new group"
            user_input = raw_input("-> ")
            if user_input == "1":
                para = {"username": self.username, "chat_name": ""}
                self.sendPDURequest("LIST", para, "CC", "")

                while not self.groupNames_received:  # waits for server response
                    pass

                if self.obj["group_fetch_success"]:
                    self.joinGroup(self.username)
                    self.obj["group_fetch_success"] = False
                    self.groupNames_received = False
                    break
                else:
                    continue

            elif user_input == "2":
                print "Enter Group name"
                groupName = raw_input("-> ")
                para = {"username": self.username, "chat_name": groupName}
                self.sendPDURequest("CHAT", para, "CC", "")

                while not self.create_group_resp_recv:         # waits for server response
                    pass

                if self.obj["groupCreated"]:
                    self.chat_name = groupName
                    print("Group Created. You have joined the group")
                    break
                else:
                    print "Group already exists"
                    continue

            else:
                print "Invalid input"
                continue

    def joinGroup(self, username):
        while True:
            user_input = raw_input("-> ")
            chatFound = False
            number = 0
            for i in range(0, len(self.groupNames)):
                try:
                    number = int(user_input)
                except ValueError:
                    print "Please enter a valid input"
                    break
                else:
                    if number == i + 1:
                        para = {"username": username, "chat_name": self.groupNames[int(user_input) - 1]}
                        self.sendPDURequest("JOIN", para, "CC", "")
                        chatFound = True
                    elif i == len(self.groupNames)-1 and not chatFound:
                        print "Please enter a valid input"
                        continue
            if not chatFound:
                continue
            else:
                break


    def displayOptions(self):
        if self.username == "":
            print "Log in first"
        else:
            print "Help         : -help"
            print "Logout       : -logout"

            if self.chat_name != "":
                print "Exit Group   : -moveout"

            if client.isAdmin:      # also check if admin of current group
                print "Ban User     : -ban"

client = ChatClient()
client.connect_to_server()

comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()

# >>> NOTE: Write all request | response related commands after this!  <<<

client.initiateDialog()

while True:
    msg = raw_input('-> ')
    if msg == "-logout":
        client.handle_close()
        break

    elif msg == "-help":
        client.displayOptions()

    elif msg == "-moveout":
        client.sendPDURequest("LEVE", {"username": client.username, "chat_name": client.chat_name}, "DC", "")

        while not client.movedOut:
            client.movedOut = False

        print ""
        client.createChatGroups()

    else:
        msg = "(" + client.username + ") " + msg
        client.sendPDURequest("MSSG", {"username": client.username, "chat_name": client.chat_name}, "DC", msg)

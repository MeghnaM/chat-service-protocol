import asynchat
import asyncore
import socket
import threading
import json
from pdu_request import PDURequest
from response_handler import ResponseHandler
import pdu_data


class ChatClient(asynchat.async_chat):
    __host = "127.0.0.1"    # IP
    # __host = "168.235.64.44"
    __port = 12345          # port that server listens to

    def __init__(self):
        """constructor for the client object"""

        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)      # creates new socket
        self.set_terminator('\n')       # async chat calls found_terminator on receival of this terminator
        self.buffer = []
        self.obj = {}
        self.username = ""
        self.chat_name = ""
        self.groupNames = []

        # region while loop terminators
        self.authentication_complete = False        # set to true when authentication is complete
        self.create_group_resp_recv = False         # create group function called and value returned
        self.groupNames_received = False
        self.ban_complete = False                   # whether the ban function has returned a value
        self.ban_allowed = False                    # whether to ban or not
        self.movedOut = False                       # whether move out of group function has returned a value
        # end region while loop terminators

    def connect_to_server(self):
        """Makes connection to the server based on host and port no"""

        self.connect((ChatClient.__host, ChatClient.__port))

    def sendPDURequest(self, command, parameters, channel, payload):
        """Creates object of class PDURequest and serializes the object to a string. 
        The string terminates with '\n' so that the servers found_terminator function would be called on invoking push
        :param command -> command that the user wants to fire
        :param parameters -> parameters required to fire the command
        :param channel -> channel in which the data is passed
        :param payload -> extra data that needs to be passed for the command
        """

        str_send = PDURequest(command, parameters, channel, payload).createRequestStr()
        self.push(str_send)

    def collect_incoming_data(self, data):
        """Used by async chat when client receives a response from the server"""

        self.buffer.append(data)

    def found_terminator(self):
        """Called when response has the value set in set_terminator in the clients constructor"""

        resp_str = ''.join(self.buffer)
        self.buffer = []

        resp_obj = json.loads(resp_str)         # deserialization | converts response string back to JSON object

        if resp_obj["response_code"] == "110":              # Authenticated successfully
            self.obj["authenticated"] = True
            self.authentication_complete = True

        elif resp_obj["response_code"] == "130":            # List of groups received
            if self.username == resp_obj["parameters"]["username"]:
                self.groupNames = resp_obj["payload"]

                self.processResponse(resp_obj)

                self.obj["group_fetch_success"] = True
                self.groupNames_received = True

        elif resp_obj["response_code"] == "140":            # Message received
            chat = resp_obj["payload"]

            if self.username == chat[1: len(self.username) + 1]:       # don't print on senders console
                return
            else:
                self.processResponse(resp_obj)
                print("-> "),       # comma added to allow next print to be on the same line

        elif resp_obj["response_code"] == "170":            # Group created successfully
            self.obj["groupCreated"] = True
            self.create_group_resp_recv = True

        elif resp_obj["response_code"] == "180":            # Group joined successfully
            if self.username == resp_obj["parameters"]["username"]:
                self.chat_name = resp_obj["parameters"]["chat_name"]
            self.processResponse(resp_obj)

        elif resp_obj["response_code"] == "190":            # Left group successfully
            self.processResponse(resp_obj)
            if resp_obj["parameters"]["username"] == self.username:
                self.movedOut = True

        elif resp_obj["response_code"] == "191":            # Banned user successfully
            if resp_obj["parameters"]["banned_user"] == self.username:
                self.chat_name = ""
            self.processResponse(resp_obj)

        elif resp_obj["response_code"] == "192":            # Kicked user successfully
            if resp_obj["parameters"]["kicked_user"] == self.username:
                self.chat_name = ""
            self.processResponse(resp_obj)

        elif resp_obj["response_code"] == "200":            # Authentication failed
            self.obj["authenticated"] = False
            self.authentication_complete = True

        elif resp_obj["response_code"] == "230":            # Group creation failed
            self.obj["groupCreated"] = False
            self.create_group_resp_recv = True

        elif resp_obj["response_code"] == "240":            # Group joining failed
            if self.username == resp_obj["parameters"]["username"]:
                self.processResponse(resp_obj)

                self.obj["group_fetch_success"] = False
                self.groupNames_received = True

        elif resp_obj["response_code"] == "250":            # Ban user failed
            if resp_obj["parameters"]["username"] == self.username:
                self.processResponse(resp_obj)

        elif resp_obj["response_code"] == "260":            # Kick user failed
            if resp_obj["parameters"]["username"] == self.username:
                self.processResponse(resp_obj)

        else:                                               # All other response codes
            self.processResponse(resp_obj)

    def processResponse(self, resp_obj):
        """Processes the response from the server i.e. appropriate function is called on the ResponseHandler class based
        on the response code"""

        resp_code = resp_obj["response_code"]
        obj = pdu_data.PDUData()
        obj.payload = resp_obj["payload"]

        resh_obj = ResponseHandler(obj)
        return resh_obj.runResponseCodeAction(resp_code)

    def handle_close(self):
        """Async chat calls this if the client has thrown an unhandled error or if the client logs out from the system"""

        self.close()
        print "Your connection has been terminated"

    def initiateDialog(self):
        """This function is responsible for clients authentication, creation or joining groups"""

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

                # Wait for server response. Value of self.authentication_complete set to true in found_terminator
                while not self.authentication_complete:
                    pass

                if self.obj["authenticated"]:
                    self.username = username
                    print("Login successful")
                    self.createOrFetchGroups()
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

                # Wait for server response. Value of self.authentication_complete set to true in found_terminator
                while not self.authentication_complete:
                    pass

                if self.obj["authenticated"]:
                    self.username = username
                    print("Account created")
                    self.createOrFetchGroups()
                    break
                else:
                    print "Username already exists"
                    continue
            else:
                print "Invalid input, try again."
                continue

    def createOrFetchGroups(self):
        """Function responsible for fetching available groups or creating a new group"""
        while True:
            print "1 -> Join available groups"
            print "2 -> Create new group"
            user_input = raw_input("-> ")
            if user_input == "1":
                para = {"username": self.username, "chat_name": ""}
                self.sendPDURequest("LIST", para, "CC", "")

                # Wait for server response. Value of self.groupNames_received set to true in found_terminator
                while not self.groupNames_received:
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

                if groupName.strip() == "":
                    print "Group name cannot be 0 characters"
                    continue

                para = {"username": self.username, "chat_name": groupName}
                self.sendPDURequest("CHAT", para, "CC", "")

                # Wait for server response. Value of self.create_group_resp_recv set to true in found_terminator
                while not self.create_group_resp_recv:
                    pass

                if self.obj["groupCreated"]:
                    self.chat_name = groupName
                    print("Group Created. You are the admin of this group. You have joined the group")
                    break
                else:
                    print "Group already exists"
                    continue

            else:
                print "Invalid input"
                continue

    def joinGroup(self, username):
        """Function responsible for joining a selected group
        :param username -> username of the client"""

        while True:
            user_input = raw_input("-> ")
            chatFound = False

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

            self.groupNames = []        # reset for next fetch
            if not chatFound:
                continue
            else:
                break

    def displayOptions(self):
        """Display list of commands that can be fired by the client. Function is called when client types in -help"""

        if self.username == "":
            print "Log in first"
        else:
            print "Help         : -help"
            print "Logout       : -logout"

            if self.chat_name == "":
                print "Join group   : -join"

            if self.chat_name != "":
                print "Exit Group   : -moveout"

            # if client.isAdmin:      # also check if admin of current group
            print "Kick User    : -kick username"
            print "Ban User     : -ban username"

    def chatConsole(self):
        """Function is responsible for displaying the chat console"""

        while True:
            msg = raw_input('-> ')
            if msg == "-logout":            # client wants to logout from the system
                self.handle_close()
                break

            elif msg == "-help":            # client wants to see the list of commands that can be fired
                self.displayOptions()

            elif msg == "-moveout":         # client wants to leave the group
                self.sendPDURequest("LEVE", {"username": self.username, "chat_name": self.chat_name}, "CC", "")

                while not self.movedOut:
                    pass

                self.movedOut = False
                print ""
                self.createOrFetchGroups()

            elif msg == "-join":            # client wants to join a new group
                if self.chat_name != "":
                    print "First run -moveout"
                else:
                    self.createOrFetchGroups()

            elif "-kick" in msg:            # admin client who wants to kick a user from the chat (user can rejoin)
                if self.chat_name == "":
                    print "You are not part of a group right now. Join a group first"
                    continue

                kick_user = msg.strip().split(" ")[1:]
                if len(kick_user) == 0:
                    print "Missing parameters. Syntax ==>  -kick username"
                elif len(kick_user) > 1:
                    print "Too many parameters. Syntax ==>  -kick username"
                elif kick_user[0] == self.username:
                    print "You cannot kick yourself"
                else:
                    parameters = {"username": client.username, "chat_name": client.chat_name, "kicked_user": kick_user[0]}
                    self.sendPDURequest("KICK", parameters, "AC", "")

            elif "-ban" in msg:             # admin client who wants to ban a user from the chat (user can't rejoin)
                if self.chat_name == "":
                    print "You are not part of a group right now. Join a group first"
                    continue

                banned = msg.strip().split(" ")[1:]
                if len(banned) == 0:
                    print "Missing parameters. Syntax ==>  -ban username"
                elif len(banned) > 1:
                    print "Too many parameters. Syntax ==>  -ban username"
                elif banned[0] == self.username:
                    print "You cannot ban yourself"
                else:
                    parameters = {"username": client.username, "chat_name": client.chat_name, "banned_user": banned[0]}
                    self.sendPDURequest("BANN", parameters, "AC", "")

            else:                           # chats sent from the client
                if self.chat_name == "":
                    print "You are not connected to any group. Try -help to see the list of the commands"
                    continue
                elif msg.strip():
                    continue

                msg = "(" + self.username + ") " + msg
                self.sendPDURequest("MSSG", {"username": self.username, "chat_name": self.chat_name}, "DC", msg)

client = ChatClient()
client.connect_to_server()

comm = threading.Thread(target=asyncore.loop)
comm.daemon = True
comm.start()

client.initiateDialog()
client.chatConsole()

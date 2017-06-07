import asynchat
import asyncore
import socket
import sys
import json
import request_handler as reqh

# client_map object is critical for the proper functioning of the protocol
# chat_room object is maintained by async chat. It has all the sockets of the clients that are connected to the server
# Our code makes use of the chat_room object and to maintain the client_map.
# The client_map is essentially a map between username and the associated socket in the chat_room

chat_room = {}          # maintained by async chat
client_map = {          # maintained by our code
    "clients": []
}


class ChatHandler(asynchat.async_chat):
    def __init__(self, sock, server_obj):
        """constructor for the ChatHandler object"""

        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
        self.set_terminator('\n')       # async chat calls found_terminator on receival of this terminator
        self.buffer = []
        self.server_obj = server_obj

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        msg = ''.join(self.buffer)
        req_obj = json.loads(msg)

        # process request and create response string
        response = self.server_obj.processRequest(req_obj, self)

        if len(client_map["clients"]) == len(chat_room) - 1:        # client in client_map is only filled once user is authenticated
            for client in client_map["clients"]:
                # when username has not been set
                if client["username"] == "":
                    if req_obj["command"] in ["NWUA", "AUTH"]:      # ignore all other commands
                        client["handler"].push(response)

                # when client has not joined a group or if is banned, kicked or moved out from group
                elif client["chat_name"] == "":
                    # chat_name = "" is only valid for below commands from the user
                    if req_obj["command"] in ["AUTH", "LIST", "JOIN", "KICK", "BANN", "LEVE", "REDY"]:
                        client["handler"].push(response)

                # send to users part of the same group
                elif client["chat_name"] == req_obj["parameters"]["chat_name"]:
                    client["handler"].push(response)

        else:       # broadcast to all
            for handler in chat_room.itervalues():
                if hasattr(handler, 'push'):
                    handler.push(response)

        self.buffer = []
        # TODO: Update close condition - only when *all* the clients have logged out,
        #       should the server connection be terminated
        if msg == "-logout":
            # TODO: remove from client_map
            self.handle_close()

    def handle_close(self):
        """Async chat calls this if the server has thrown an unhandled error or if the server wants to terminate"""
        self.close()
        print "Server session has been terminated"
        sys.exit(0)


class ChatServer(asyncore.dispatcher):
    __host = "127.0.0.1"                    # Server IP
    __port = 12345                          # Server listening of this port
    __user_file = "./user_accounts.txt"     # User credentials
    __list = "./list.txt"                   # Group details

    def __init__(self):
        """Initialises the server, and listener is activated"""

        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((ChatServer.__host, ChatServer.__port))
        self.listen(5)
        print 'Server listening on ', ChatServer.__host, ':', ChatServer.__port

    def handle_accept(self):
        """Async chat calls this method when a client connects to the server"""

        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock, self)

    def processRequest(self, req_obj, handler):
        """Processes the requests from the client i.e. appropriate function is called on the RequestHandler class based
        on the command"""

        command = req_obj["command"]

        # preparing obj to be used by RequestHandler functions
        obj = {
            "username": req_obj["parameters"]["username"]
        }
        if command == "AUTH" or command == "NWUA":
            obj["password"] = req_obj["parameters"]["password"]
            obj["filename"] = self.__user_file

        elif command == "LIST":
            obj["list"] = self.__list

        elif command == "CHAT":
            obj["chat_name"] = req_obj["parameters"]["chat_name"]
            obj["list"] = self.__list

        elif command == "JOIN":
            obj["chat_name"] = req_obj["parameters"]["chat_name"]
            obj["list"] = self.__list

        elif command == "BANN":
            obj["chat_name"] = req_obj["parameters"]["chat_name"]
            obj["banned_user"] = req_obj["parameters"]["banned_user"]
            obj["filename"] = self.__user_file
            obj["list"] = self.__list

        elif command == "KICK":
            obj["chat_name"] = req_obj["parameters"]["chat_name"]
            obj["kicked_user"] = req_obj["parameters"]["kicked_user"]
            obj["filename"] = self.__user_file
            obj["list"] = self.__list

        elif command == "MSSG":
            obj["payload"] = req_obj["payload"]

        reqh_obj = reqh.RequestHandler(obj)
        return reqh_obj.run_command(command, handler, client_map)           # returns response string

server = ChatServer()
asyncore.loop(map=chat_room)

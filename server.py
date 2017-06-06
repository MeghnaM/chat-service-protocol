import asynchat
import asyncore
import socket
import sys
import json
import request_handler as reqh

chat_room = {}
client_map = {
    "clients": []
}


class ChatHandler(asynchat.async_chat):
    def __init__(self, sock, server_obj):
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
        self.set_terminator('\n')
        self.buffer = []
        self.server_obj = server_obj

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):     # for broadcasting
        msg = ''.join(self.buffer)
        req_obj = json.loads(msg)
        response = self.server_obj.processRequest(req_obj, self)

        if len(client_map["clients"]) == len(chat_room) - 1:        # client is only filled when user is authenticated
            for client in client_map["clients"]:
                if client["username"] == "" or client["chat_name"] == "" and req_obj["command"] != "MSSG":
                    client["handler"].push(response)
                elif client["chat_name"] != "" and client["chat_name"] == req_obj["parameters"]["chat_name"]:
                    client["handler"].push(response)

        else:
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
        self.close()
        print "Server session has been terminated"
        sys.exit(0)


class ChatServer(asyncore.dispatcher):
    __host = "127.0.0.1"
    __port = 12345
    __filename = "./user_accounts.txt"
    __list = "./list.txt"

    def __init__(self):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((ChatServer.__host, ChatServer.__port))
        self.listen(5)
        print 'Server listening on ', ChatServer.__host, ':', ChatServer.__port

    def getFileName(self):
        return self.__filename

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock, self)

    def processRequest(self, req_obj, handler):
        command = req_obj["command"]
        list = {}
        # TODO: Validate command i.e. check if command exists and if command is valid for current state
        obj = {}
        if command == "AUTH" or command == "NWUA":
            obj["username"] = req_obj["parameters"]["username"]
            obj["password"] = req_obj["parameters"]["password"]
            obj["filename"] = self.__filename

        elif command == "LIST":
            obj["username"] = req_obj["parameters"]["username"]
            obj["list"] = self.__list

        elif command == "CHAT":
            obj["username"] = req_obj["parameters"]["username"]
            obj["chat_name"] = req_obj["parameters"]["chat_name"]
            obj["list"] = self.__list

        elif command == "JOIN":
            obj["username"] = req_obj["parameters"]["username"]
            obj["chat_name"] = req_obj["parameters"]["chat_name"]
            obj["list"] = self.__list

        elif command == "LEVE":
            obj["username"] = req_obj["parameters"]["username"]

        elif command == "MSSG":
            obj["payload"] = req_obj["payload"]

        reqh_obj = reqh.RequestHandler(obj)
        return reqh_obj.run_command(command, handler, client_map)        # returns response string

server = ChatServer()
asyncore.loop(map=chat_room)

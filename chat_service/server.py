import asynchat
import asyncore
import socket
import sys
import json
import request_handler as reqh
import PDUResponse

chat_room = {}


class ChatHandler(asynchat.async_chat):
    def __init__(self, sock, server_obj):
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
        self.set_terminator('\n')
        self.buffer = []
        self.server_obj = server_obj

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        msg = ''.join(self.buffer)
        req_obj = json.loads(msg)
        response = self.server_obj.processRequest(req_obj)
        response += "\n"

        for handler in chat_room.itervalues():
            if hasattr(handler, 'push'):
                handler.push(response)

        self.buffer = []
        # TODO: Update close condition - only when *all* the clients have logged out,
        #       should the server connection be terminated
        if msg == "logout":
            self.handle_close()

    def handle_close(self):
        self.close()
        print "Server session has been terminated"
        sys.exit(0)


class ChatServer(asyncore.dispatcher):
    __host = "127.0.0.1"
    __port = 12345

    def __init__(self):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((ChatServer.__host, ChatServer.__port))
        self.listen(5)
        print 'Server listening on ', ChatServer.__host, ':', ChatServer.__port

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock, self)

    def processRequest(self, req_obj):
        command = req_obj["command"]

        # TODO: Validate command i.e. check if command exists and if command is valid for current state

        reqh_obj = reqh.RequestHandler()
        resp_code = reqh_obj.reqs_dict[command]

        if resp_code == "100":
            params = []
            control = "CC"
            payload = "Ready!"

        elif resp_code ==  "140":
            params = []
            control = "DC"
            payload = req_obj["payload"]

        else:
            params = []
            control = "DC"
            payload = ""

        return self.createResponse(resp_code, params, control, payload)

    def createResponse(self, resp_code, params, control, payload):
        resp_obj = PDUResponse.PDUResponse(resp_code, params, control, payload)
        str_resp = json.dumps(resp_obj.__dict__)     # serializing
        return str_resp

server = ChatServer()
asyncore.loop(map=chat_room)

PDUDataclass RequestHandler:

    def __init__(self):
        self.reqs_dict = {
            "REDY": self.readyAction(PDUData),
            "NICK": self.nickAction(PDUData),
            "JOIN": self.joinAction(PDUData),
            "PART": self.partAction(PDUData),
            "MSSG": self.mssgAction(PDUData),
            "KICK": self.kickAction(PDUData),
            "BANK": self.banAction(PDUData),
            "BLAK": self.blackAction(PDUData),
            "ELVT": self.elevateAction(PDUData),
            "DROP": self.dropAction(PDUData),
            "LIST": self.listAction(PDUData),
            "PMSG": self.privateMessageAction(PDUData),
            "PRVM": self.endPrivateMessageAction(PDUData),
            "PMSS": self.sendPrivateMessageAction(PDUData),
            "MAIL": self.mailAction(PDUData),
            "QUIT": self.quitAction(PDUData),
            "KEEP": self.keepAliveAction(PDUData)
        }

    # readyAction sends a REDY PDU to the server
    def readyAction(self):
        print("Ready called")
        return "100"

    # nickAction sends a NICK PDU to the server
    def nickAction(self):
        pass

    # joinAction sends a JOIN PDU to the server
    def joinAction(self):
        #parameters nick and chatname
        #server adds nick to chat_room user list
        #client opens chat room window
        pass

    def partAction(self):
        #parameters nick and chatname
        #server removes nick from chat_Room list
        #client closes chatroom window 
        pass

    def mssgAction(self):
        #parameters nick, chatname, ascii text
        #server recfeives ascoo text and broadcasts across chatrooom
        
        pass

    def kickAction(self):
        pass

    def banAction(self):
        pass

    def blackAction(self):
        pass

    def elevateAction(self):
        #parameters nick and chatname
        #server adds nick to elevated user list for the chat room object
        pass

    def dropAction(self):
        #parameters nick and chatname
        #server removes nick from elevated user list for the chat room object
        pass

    def listAction(self):
        #parameters nick
        #server sends a list of chatrooms from the global chat room object
        pass

    def privateMessageAction(self):
        pass

    def endPrivateMessageAction(self):
        pass

    def sendPrivateMessageAction(self):
        pass

    def mailAction(self):
        #parameters - nick
        #server responds with asciii text payload of queued messages
        pass

    def quitAction(self):
        #paremte3rs nick
        #server disconnect
        pass

    def keepAliveAction(self):
        pass


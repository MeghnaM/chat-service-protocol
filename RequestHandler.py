class RequestHandler:

    pduData = PDUData()

    def __init__(self):
        self.reqs_dict = {
            "REDY": self.readyAction(pduData),
            "NICK": self.nickAction(pduData),
            "JOIN": self.joinAction(pduData),
            "PART": self.partAction(pduData),
            "MSSG": self.mssgAction(pduData),
            "KICK": self.kickAction(pduData),
            "BANK": self.banAction(pduData),
            "BLAK": self.blackAction(pduData),
            "ELVT": self.elevateAction(pduData),
            "DROP": self.dropAction(pduData),
            "LIST": self.listAction(pduData),
            "PMSG": self.privateMessageAction(pduData),
            "PRVM": self.endPrivateMessageAction(pduData),
            "PMSS": self.sendPrivateMessageAction(pduData),
            "MAIL": self.mailAction(pduData),
            "QUIT": self.quitAction(pduData),
            "KEEP": self.keepAliveAction(pduData)
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
        joinchat(PDUData)
        

    def partAction(self):
        #parameters nick and chatname
        #server removes nick from chat_Room list
        #client closes chatroom window
        partchat(PDUData)
        

    def mssgAction(self):
        #parameters nick, chatname, ascii text
        #server recfeives ascoo text and broadcasts across chatrooom
        messagechat()
        

    def kickAction(self):
        kickchat()
        

    def banAction(self):
        banchat()

    def blackAction(self):
        blackchat()

    def elevateAction(self):
        #parameters nick and chatname
        #server adds nick to elevated user list for the chat room object
        elevatechat()
        

    def dropAction(self):
        #parameters nick and chatname
        #server removes nick from elevated user list for the chat room object
        dropchat()

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
        mailchat()
        #parameters - nick
        #server responds with asciii text payload of queued messages

    def quitAction(self):
        #paremte3rs nick
        #server disconnect
        quitchat()
        

    def keepAliveAction(self):
        pass


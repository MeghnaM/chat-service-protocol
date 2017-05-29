class RequestHandler:

    def __init__(self):
        self.reqs_dict = {
            "REDY": self.readyAction(),
            "NICK": self.nickAction(),
            "JOIN": self.joinAction(),
            "PART": self.partAction(),
            "MSSG": self.mssgAction(),
            "KICK": self.kickAction(),
            "BANK": self.banAction(),
            "BLAK": self.blackAction(),
            "ELVT": self.elevateAction(),
            "DROP": self.dropAction(),
            "LIST": self.listAction(),
            "PMSG": self.privateMessageAction(),
            "PRVM": self.endPrivateMessageAction(),
            "PMSS": self.sendPrivateMessageAction(),
            "MAIL": self.mailAction(),
            "QUIT": self.quitAction(),
            "KEEP": self.keepAliveAction()
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
        pass

    def partAction(self):
        pass

    def mssgAction(self):
        pass

    def kickAction(self):
        pass

    def banAction(self):
        pass

    def blackAction(self):
        pass

    def elevateAction(self):
        pass

    def dropAction(self):
        pass

    def listAction(self):
        pass

    def privateMessageAction(self):
        pass

    def endPrivateMessageAction(self):
        pass

    def sendPrivateMessageAction(self):
        pass

    def mailAction(self):
        pass

    def quitAction(self):
        pass

    def keepAliveAction(self):
        pass


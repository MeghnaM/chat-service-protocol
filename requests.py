

#readyAction sends a REDY PDU to the server

def readyAction():
    pass

#nickAction sends a NICK PDU to the server

def nickAction():
    pass

#joinAction sends a JOIN PDU to the server

def joinAction():
    pass

def partAction():
    pass

def mssgAction():
    pass

def kickAction():
    pass

def banAction():
    pass

def blackAction():
    pass

def elevateAction():
    pass

def dropAction():
    pass

def listAction():
    pass

def privateMessageAction():
    pass

def endPrivateMessageAction():
    pass

def sendPrivateMessageAction():
    pass

def mailAction():
    pass

def quitAction():
    pass

def keepAliveAction():
    pass


reqs_dict = {
    "REDY": readyAction(),
    "NICK": nickAction(),
    "JOIN": joinAction(),
    "PART": partAction(),
    "MSSG": mssgAction(),
    "KICK": kickAction(),
    "BANK": banAction(),
    "BLAK": blackAction(),
    "ELVT": elevateAction(),
    "DROP": dropAction(),
    "LIST": listAction(),
    "PMSG": privateMessageAction(),
    "PRVM": endPrivateMessageAction(),
    "PMSS": sendPrivateMessageAction(),
    "MAIL": mailAction(),
    "QUIT": quitAction(),
    "KEEP": keepAliveAction()
}

#def parsePDUs(self, PDU):
#    reqs_dict(PDU)

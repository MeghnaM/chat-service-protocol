def readyAction():
    pass

def nickAction():
    pass

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


dict_reqs = {
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
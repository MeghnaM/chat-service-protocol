import json


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
            "KEEP": self.keepAliveAction(),

            "NWUA": self.createNewUserAccount(),
            "AUTH": self.loginAuthentication()
        }

    def createNewUserAccount(self):
        # s = serv.ChatServer()
        # users_str = s.getCredentials(s.getFileName).strip()
        # if users_str is not None and users_str:
        #     all_users_obj = json.loads(users_str)
        # else:
        #     all_users_obj = {"users": []}

        # if len(all_users_obj["users"]) == 0:
        #     print "We don't have your account in our system"
        #     continue
        # else:
        #     valid_user = False
        #     for user in all_users_obj["users"]:
        #         if user["username"] == username and user["password"] == password:
        #             valid_user = True
        #             break
        #
        #     if valid_user:
        #         print("Login successful")
        #         break
        #     else:
        #         print "Either your username or password is incorrect"
        #         continue
        return 110

    def loginAuthentication(self):
        return "110"

    # readyAction sends a REDY PDU to the server
    def readyAction(self):
        print "Ready called"
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
        print "Message action called"
        return "140"

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

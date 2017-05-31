import json
import os
from user import User


class RequestHandler:
    def __init__(self, obj=None):
        self.obj = obj

    def run_command(self, command):
        # changed from dictionary because all the functions were being called when RequestHandler was being instantiated
        if command == "REDY":
            return self.readyAction()
        elif command == "NICK":
            return self.nickAction()
        elif command == "JOIN":
            return self.joinAction()
        elif command == "PART":
            return self.partAction()
        elif command == "MSSG":
            return self.mssgAction()
        elif command == "KICK":
            return self.kickAction()
        elif command == "BANK":
            return self.banAction()
        elif command == "BLAK":
            return self.blackAction()
        elif command == "ELVT":
            return self.elevateAction()
        elif command == "DROP":
            return self.dropAction()
        elif command == "LIST":
            return self.listAction()
        elif command == "PMSG":
            return self.privateMessageAction()
        elif command == "PRVM":
            return self.endPrivateMessageAction()
        elif command == "PMSS":
            return self.sendPrivateMessageAction()
        elif command == "QUIT":
            return self.quitAction()
        elif command == "KEEP":
            return self.keepAliveAction()
        elif command == "AUTH":
            return self.loginAuthentication()
        elif command == "NWUA":
            return self.createNewUserAccount()

    def getCredentialFile(self, filename):
        if not os.path.isfile('./' + filename):
            file = open(filename, "w+")
            file.close()
            return ""

        else:
            with open(filename, 'r') as myfile:
                data = myfile.read().replace('\n', '')
            return data

    def createNewUserAccount(self):
        users_str = self.getCredentialFile(self.obj["filename"]).strip()
        if users_str is not None and users_str:
            all_users_obj = json.loads(users_str)
        else:
            all_users_obj = {"users": []}

        for user_acc in all_users_obj["users"]:
            if user_acc["username"] == self.obj["username"]:
                return "200"

        new_user = User(self.obj["username"], self.obj["password"])
        all_users_obj["users"].append(json.loads(json.dumps(new_user.__dict__)))

        file = open(self.obj["filename"], "w")
        file.write(json.dumps(all_users_obj))
        file.close()

        return "110"

    def loginAuthentication(self):
        users_str = self.getCredentialFile(self.obj["filename"]).strip()

        if users_str is not None and users_str:
            all_users_obj = json.loads(users_str)
        else:
            all_users_obj = {"users": []}

        if len(all_users_obj["users"]) == 0:
            return "200"
        else:
            valid_user = False
            for user_acc in all_users_obj["users"]:
                if user_acc["username"] == self.obj["username"] and user_acc["password"] == self.obj["password"]:
                    valid_user = True
                    break

            if valid_user:
                return "110"
            else:
                print "Either your username or password is incorrect"
                return "200"

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

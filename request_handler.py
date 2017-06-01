import json
import os
from user import User
from chat_room import Chat_room
from pdu_response import PDUResponse


class RequestHandler:
    def __init__(self, req_obj=None):
        self.obj = req_obj

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
        elif command == "CHAT":
            return self.createNewChat()

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
                return PDUResponse("200", {}, "", "").createResponseStr()

        new_user = User(self.obj["username"], self.obj["password"])
        all_users_obj["users"].append(json.loads(json.dumps(new_user.__dict__)))
        file = open(self.obj["filename"], "w")
        file.write(json.dumps(all_users_obj))
        file.close()

        return PDUResponse("110", {}, "CC", "").createResponseStr()

    def loginAuthentication(self):
        users_str = self.getCredentialFile(self.obj["filename"]).strip()

        if users_str is not None and users_str:
            all_users_obj = json.loads(users_str)
        else:
            all_users_obj = {"users": []}

        if len(all_users_obj["users"]) == 0:
            return PDUResponse("200", {}, "CC", "").createResponseStr()
        else:
            valid_user = False
            for user_acc in all_users_obj["users"]:
                if user_acc["username"] == self.obj["username"] and user_acc["password"] == self.obj["password"]:
                    valid_user = True
                    break

            if valid_user:
                return PDUResponse("110", {}, "CC", "").createResponseStr()
            else:
                print "Either your username or password is incorrect"
                return PDUResponse("200", {}, "CC", "").createResponseStr()

    # readyAction sends a REDY PDU to the server
    def readyAction(self):
        print "Ready called"
        return PDUResponse("100", {}, "CC", "Ready").createResponseStr()

    # nickAction sends a NICK PDU to the server
    def nickAction(self):
        pass

    # joinAction sends a JOIN PDU to the server
    def joinAction(self):
        # parameters nick and chatname
        # server adds nick to chat_room user list
        # client opens chat room window
        chat_para = self.getListFile(self.obj["list"]).strip()

        all_chat_obj = json.loads(chat_para)
        for user_acc in all_chat_obj["chats"]:
            users = user_acc["users"]
            for i in range(0, len(users)):
                if users[i] == self.obj["username"]:
                    break
                elif len(users) - 1 == i and users[i] != self.obj["username"]:
                    users.append(self.obj["username"])
            user_acc["users"] = users

        file = open(self.obj["list"], "w")
        file.write(json.dumps(all_chat_obj))
        file.close()

        f = open("user_accounts.txt")
        data = f.read().replace('\n', '').strip()
        all_users_obj = json.loads(data)
        for user_acc in all_users_obj["users"]:
            if user_acc["username"] == self.obj["username"]:
                user_acc["isAdmin"] = True
                adminGroups = user_acc["adminGroups"]
                for i in range(0, len(adminGroups)):
                    if adminGroups[i] == self.obj["chat_name"]:
                        break
                    if len(adminGroups) - 1 == i:
                        adminGroups.append(self.obj["chat_name"])
                if len(adminGroups) == 0:
                    adminGroups.append(self.obj["chat_name"])
                break
        f.close()
        file = open("user_accounts.txt", "w")
        file.write(json.dumps(all_users_obj))
        file.close()
        return PDUResponse("180", {}, "", self.obj["username"]).createResponseStr()

    def partAction(self):
        #parameters nick and chatname
        #server removes nick from chat_Room list
        #client closes chatroom window
        pass

    def mssgAction(self):
        #parameters nick, chatname, ascii text
        #server recfeives ascoo text and broadcasts across chatrooom
        print "Message action called"
        return PDUResponse("140", {}, "DC", self.obj["payload"]).createResponseStr()

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
        # parameters nick
        # server sends a list of chatrooms from the global chat room object
        chat_para = self.getListFile(self.obj["list"]).strip()

        if chat_para != "":
            all_users_obj = json.loads(chat_para)
            groupList = []
            for user_acc in all_users_obj["chats"]:
                groupList.append(user_acc["chat_name"])
            return PDUResponse("130", {"username": self.obj["username"]}, "", groupList).createResponseStr()

        else:
            return PDUResponse("240", {"username": self.obj["username"]}, "", "There are currently no groups").createResponseStr()

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

    def getListFile(self, list):
        if not os.path.isfile('./' + list):
            file = open(list, "w+")
            file.close()
            return "{}"

        else:
            with open(list, 'r') as myfile:
                data = myfile.read().replace('\n', '')
            return data

    def createNewChat(self):
        chat_para = self.getListFile(self.obj["list"]).strip()
        if chat_para is not None and chat_para:
            all_chat_obj = json.loads(chat_para)
        else:
            all_chat_obj = {"chats": []}

        for groupChat in all_chat_obj["chats"]:
            if groupChat["chat_name"] == self.obj["chat_name"]:
                print "Duplicate groups"
                return PDUResponse("230", {}, "", "Group name already exists").createResponseStr()
            else:
                print "Not found in this loop"

        users = [self.obj["username"]]
        admins = [self.obj["username"]]
        new_user = Chat_room(self.obj["chat_name"], users, admins)
        all_chat_obj["chats"].append(json.loads(json.dumps(new_user.__dict__)))

        file = open(self.obj["list"], "w")
        file.write(json.dumps(all_chat_obj))
        file.close()

        f = open("user_accounts.txt")
        data = f.read().replace('\n', '').strip()
        all_users_obj = json.loads(data)
        for user_acc in all_users_obj["users"]:
            if user_acc["username"] == self.obj["username"]:
                user_acc["isAdmin"] = True
                adminGroups = user_acc["adminGroups"]
                for i in range(0, len(adminGroups)):
                    if adminGroups[i] == self.obj["chat_name"]:
                        break
                    if len(adminGroups) - 1 == i:
                        adminGroups.append(self.obj["chat_name"])
                if len(adminGroups) == 0:
                    adminGroups.append(self.obj["chat_name"])
                break
        f.close()
        file = open("user_accounts.txt", "w")
        file.write(json.dumps(all_users_obj))
        file.close()

        return PDUResponse("170", {}, "", "").createResponseStr()

    def getList(self):
        pass

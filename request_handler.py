import json
import os
from user import User
from chat_room import Chat_room
from pdu_response import PDUResponse


class RequestHandler:
    """RequestHandler class is used by the server to handle all the incoming requests from the client"""

    def __init__(self, req_obj=None):
        self.obj = req_obj

    def run_command(self, command, handler, client_map):
        """Calls the associated function of the command
        :param command -> command fired by the client
        :param handler -> the client socket
        :param client_map -> map of username and the client socket"""

        if command == "REDY":
            return self.readyAction()
        elif command == "NICK":
            return self.nickAction()
        elif command == "JOIN":
            return self.joinAction(handler, client_map)
        elif command == "PART":
            return self.partAction()
        elif command == "MSSG":
            return self.mssgAction()
        elif command == "KICK":
            return self.kickAction(client_map)
        elif command == "BANN":
            return self.banAction(client_map)
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
            return self.loginAuthentication(handler, client_map)
        elif command == "NWUA":
            return self.createNewUserAccount(handler, client_map)
        elif command == "CHAT":
            return self.createNewChat(handler, client_map)
        elif command == "LEVE":
            return self.leaveChat(handler, client_map)

    def getFileContents(self, filename):
        """Reads and returns contents of filename"""

        if not os.path.isfile('./' + filename):
            file = open(filename, "w+")
            file.close()
            return ""

        else:
            with open(filename, 'r') as myfile:
                data = myfile.read().replace('\n', '')
            return data

    def createNewUserAccount(self, handler, client_map):
        """Creates new user account and saves it to file"""

        # fetching file contents
        users_str = self.getFileContents(self.obj["filename"]).strip()
        if users_str is not None and users_str:
            all_users_obj = json.loads(users_str)
        else:
            all_users_obj = {"users": []}

        # checking if user already exists
        for user_acc in all_users_obj["users"]:
            if user_acc["username"] == self.obj["username"]:
                return PDUResponse("200", {}, "", "").createResponseStr()       # username already exists

        # creating new user and updating the users file
        new_user = User(self.obj["username"], self.obj["password"])
        all_users_obj["users"].append(json.loads(json.dumps(new_user.__dict__)))
        file = open(self.obj["filename"], "w")
        file.write(json.dumps(all_users_obj))
        file.close()

        # maintaining client_map object
        client_map["clients"].append({
            "username": self.obj["username"],
            "chat_name": "",
            "handler": handler
        })

        return PDUResponse("110", {}, "CC", "").createResponseStr()             # new user created

    def loginAuthentication(self, handler, client_map):
        """Authenticates user based on given credentials"""
        users_str = self.getFileContents(self.obj["filename"]).strip()

        if users_str is not None and users_str:
            all_users_obj = json.loads(users_str)
        else:
            all_users_obj = {"users": []}

        if len(all_users_obj["users"]) == 0:        # no user data available
            return PDUResponse("200", {}, "CC", "").createResponseStr()
        else:
            valid_user = False

            # checking if credentials are correct
            for user_acc in all_users_obj["users"]:
                if user_acc["username"] == self.obj["username"] and user_acc["password"] == self.obj["password"]:
                    valid_user = True
                    break

            if valid_user:
                # maintaining client_map object
                client_map["clients"].append({
                    "username": self.obj["username"],
                    "chat_name": "",
                    "handler": handler
                })

                return PDUResponse("110", {}, "CC", "").createResponseStr()             # Authenticated
            else:
                print "Either your username or password is incorrect"
                return PDUResponse("200", {}, "CC", "").createResponseStr()             # Invalid credentials

    def readyAction(self):
        """Function to check if server is alive"""
        return PDUResponse("100", {}, "CC", "Ready").createResponseStr()                # Server is ready

    # nickAction sends a NICK PDU to the server
    def nickAction(self):
        pass

    # joinAction sends a JOIN PDU to the server
    def joinAction(self, handler, client_map):
        """Function responsible for allowing client to join a group"""

        chat_para = self.getFileContents(self.obj["list"]).strip()

        all_chat_obj = json.loads(chat_para)
        isBanned = False

        # checking if joining user is banned from the group
        for chat in all_chat_obj["chats"]:
            if chat["chat_name"] == self.obj["chat_name"] and self.obj["username"] in chat["banned_users"]:
                isBanned = True
                break

        if not isBanned:
            file = open(self.obj["list"], "w")
            file.write(json.dumps(all_chat_obj))
            file.close()

            # TODO: @Shivam -> Also update userfile

            for client in client_map["clients"]:
                if client["username"] == self.obj["username"]:
                    client["chat_name"] = self.obj["chat_name"]
                    client["handler"] = handler

            parameters = {"username": self.obj["username"], "chat_name": self.obj["chat_name"]}
            return PDUResponse("180", parameters, "CC", self.obj["username"] + " has joined the group").createResponseStr()

        else:
            parameters = {"username": self.obj["username"], "chat_name": self.obj["chat_name"]}
            return PDUResponse("240", parameters, "CC", "You are banned from joining this group").createResponseStr()

    def partAction(self):
        # parameters nick and chatname
        # server removes nick from chat_Room list
        # client closes chatroom window
        pass

    def mssgAction(self):
        """Receive message from client and creating response to send to all other clients in the group"""

        return PDUResponse("140", {}, "DC", self.obj["payload"]).createResponseStr()

    def kickAction(self, client_map):
        """Function for kicking username from a group. Can only be performed by an admin. Username can rejoin"""
        groups_str = self.getFileContents(self.obj["list"]).strip()

        if groups_str is not None and groups_str:
            groups_obj = json.loads(groups_str)
        else:
            groups_obj = {"chats": []}

        isAdmin = False

        # checking if client is admin
        for chat in groups_obj["chats"]:
            if chat["chat_name"] == self.obj["chat_name"]:
                for admin in chat["admins"]:
                    if admin == self.obj["username"]:
                        isAdmin = True
                        break
                break

        if isAdmin:
            # TODO: maintain the kicks?

            # maintaining client_map object
            for client in client_map["clients"]:
                if client["username"] == self.obj["kicked_user"]:
                    client["chat_name"] = ""
                    client["handler"].chat_name = ""

            parameters = {"kicked_user": self.obj["kicked_user"]}
            return PDUResponse("192", parameters, "CC", self.obj["kicked_user"] + " has been kicked from the group")\
                .createResponseStr()

        else:
            return PDUResponse("260", {"username": self.obj["username"]}, "CC", "You are not the admin of this group") \
                .createResponseStr()

    def banAction(self, client_map):
        """Function for banning username from a group. Can only be performed by an admin. Username cannot rejoin"""

        users_str = self.getFileContents(self.obj["filename"]).strip()
        groups_str = self.getFileContents(self.obj["list"]).strip()

        if users_str is not None and users_str:
            all_users_obj = json.loads(users_str)
        else:
            all_users_obj = {"users": []}

        if groups_str is not None and groups_str:
            groups_obj = json.loads(groups_str)
        else:
            groups_obj = {"chats": []}

        isAdmin = False

        # checking if admin
        for chat in groups_obj["chats"]:
            if chat["chat_name"] == self.obj["chat_name"]:
                for admin in chat["admins"]:
                    if admin == self.obj["username"]:
                        isAdmin = True

                        # adding to list of banned users of the group
                        chat["banned_users"].append(self.obj["banned_user"])
                        break
                break

        if isAdmin:
            # updating users account
            for user_acc in all_users_obj["users"]:
                if user_acc["username"] == self.obj["banned_user"]:
                    # user accounts maintaining list of groups banned from
                    user_acc["bannedGroups"].append(self.obj["chat_name"])
                    break

            # writing back the updated user accounts and group details to the files
            file = open(self.obj["filename"], "w")
            file.write(json.dumps(all_users_obj))
            file.close()

            file = open(self.obj["list"], "w")
            file.write(json.dumps(groups_obj))
            file.close()

            # maintaining client_map object
            for client in client_map["clients"]:
                if client["username"] == self.obj["banned_user"]:
                    client["chat_name"] = ""
                    client["handler"].chat_name = ""

            return PDUResponse("191", {"banned_user": self.obj["banned_user"]}, "CC",
                               self.obj["banned_user"] + " has been banned from the group").createResponseStr()

        else:
            return PDUResponse("250", {"username": self.obj["username"]}, "CC", "You are not the admin of this group")\
                .createResponseStr()

    def blackAction(self):
        pass

    def elevateAction(self):
        # parameters nick and chatname
        # server adds nick to elevated user list for the chat room object
        pass

    def dropAction(self):
        # parameters nick and chatname
        # server removes nick from elevated user list for the chat room object
        pass

    def listAction(self):
        """Returns list of existing groups available in the server"""
        chat_para = self.getFileContents(self.obj["list"]).strip()
        if chat_para is not None and chat_para:
            all_chat_obj = json.loads(chat_para)
            groupList = []
            for user_acc in all_chat_obj["chats"]:
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
        # parameters - nick
        # server responds with asciii text payload of queued messages
        pass

    def quitAction(self):
        # paremters nick
        # server disconnect
        pass

    def keepAliveAction(self):
        pass

    def createNewChat(self, handler, client_map):
        """Creates new group and maintains the groups in a file"""

        # load file text
        chat_para = self.getFileContents(self.obj["list"]).strip()
        if chat_para is not None and chat_para:
            all_chat_obj = json.loads(chat_para)
        else:
            all_chat_obj = {"chats": []}

        # checking if group already exists
        for groupChat in all_chat_obj["chats"]:
            if groupChat["chat_name"] == self.obj["chat_name"]:
                print "Duplicate groups"
                return PDUResponse("230", {}, "", "Group name already exists").createResponseStr()

        users = [self.obj["username"]]
        admins = [self.obj["username"]]
        new_user = Chat_room(self.obj["chat_name"], users, admins)
        all_chat_obj["chats"].append(json.loads(json.dumps(new_user.__dict__)))

        # updating files with new group details
        file = open(self.obj["list"], "w")
        file.write(json.dumps(all_chat_obj))
        file.close()

        f = open("user_accounts.txt")
        data = f.read().replace('\n', '').strip()
        all_users_obj = json.loads(data)
        for user_acc in all_users_obj["users"]:
            if user_acc["username"] == self.obj["username"]:
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

        # maintaining client_map object
        for client in client_map["clients"]:
            if client["username"] == self.obj["username"]:
                client["chat_name"] = self.obj["chat_name"]
                client["handler"] = handler

        return PDUResponse("170", {}, "", "").createResponseStr()       # new group created

    def getList(self):
        pass

    def leaveChat(self, handler, client_map):
        """Function responsible for removing user from chat room"""

        for client in client_map["clients"]:
            if client["username"] == self.obj["username"]:
                client["chat_name"] = ""
                client["handler"] = handler
                break

        return PDUResponse("190", {"username": self.obj["username"]}, "",
                           self.obj["username"] + " has left the chat room").createResponseStr()

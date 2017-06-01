class Chat_room:
    def __init__(self, groupName, users, admins, banned_users=[], black_users=[]):
        self.chat_name = groupName
        self.users = users
        self.admins = admins
        self.banned_users = banned_users
        self.black_users = black_users

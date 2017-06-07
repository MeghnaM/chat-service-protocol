class User:
    def __init__(self, username, password, isAdmin=False, adminGroups=[], isBanned=False, bannedGroups=[]):
        self.username = username
        self.password = password
        self.adminGroups = adminGroups
        self.bannedGroups = bannedGroups

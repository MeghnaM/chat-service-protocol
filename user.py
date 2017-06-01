class User:
    def __init__(self, username, password, isAdmin=False, adminGroups=[], isBanned=False, bannedGroups=[]):
        self.username = username
        self.password = password
        self.isAdmin = isAdmin
        self.adminGroups = adminGroups
        self.isBanned = isBanned
        self.bannedGroups = bannedGroups

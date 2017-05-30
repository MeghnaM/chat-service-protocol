class user:
    
    def __init__(self, username, password, isAdmin = False, adminGroups = []):
        self.username = username
        self.password = password
        self.isAdmin = isAdmin
        self.adminGroups = adminGroups
        # channels_attending = []
        # mail = deque
        
        
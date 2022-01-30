class User:
    def __init__(self, username, roomID, winnings, user_type) -> None:
        self.username = username
        self.roomID = roomID
        self.winnings = winnings
        self.user_type = user_type

    def getJSON(self):
        return self.__dict__
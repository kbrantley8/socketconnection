from models.user import User

import random

cardIndex = [
    "2C", "2D", "2H", "2S",
    "3C", "3D", "3H", "3S",
    "4C", "4D", "4H", "4S",
    "5C", "5D", "5H", "5S",
    "6C", "6D", "6H", "6S",
    "7C", "7D", "7H", "7S",
    "8C", "8D", "8H", "8S",
    "9C", "9D", "9H", "9S",
    "10C", "10D", "10H", "10S",
    "JC", "JD", "JH", "JS",
    "QC", "QD", "QH", "QS",
    "KC", "KD", "KH", "KS"
]
class Room:
    def __init__(self, roomID: str, host_username: str, host_user_info: User) -> None:
        self.roomID = roomID
        self.players = { host_username: host_user_info.getJSON() }
        self.host = host_username
        self.horses = {
            "AC": {
                "name": "",
                "bets": {},
                'position': 0
            },
            "AD": {
                "name": "",
                "bets": {},
                'position': 0
            },
            "AH": {
                "name": "",
                "bets": {},
                'position': 0
            },
            "AS": {
                "name": "",
                "bets": {},
                'position': 0
            }
        }
        self.playerOrder = []
        self.currentIndex = 0
        self.settings = {
            'bet_min': 1,
            'bet_max': 10,
            'trackLength': 7
        }
        self.metric = 'drinks'
        self.currentCard = 'back'
        self.usedCards = []
        self.inProgress = False
        self.gameStatus = 0

    def addPlayer(self, player):
        self.players[player.username] = player.getJSON()
    
    def removePlayer(self, player):
        del self.players[player.username]

    def randomizePlayerOrder(self):
        usernames = list(self.players.keys())
        random.shuffle(usernames)
        self.playerOrder = usernames
        self.currentIndex = 0
        self.gameStatus = 1
    
    def placeBet(self, horse_id, player, wager, horse_name):
        horse = self.horses[horse_id]
        if (len(horse['name']) == 0):
            horse['name'] = horse_name
        
        horse['bets'][player['username']] = wager
        self.horses[horse_id] = horse
        
    def changeBetTurn(self):
        self.currentIndex = self.currentIndex + 1

    def startGame(self):
        self.inProgress = True
        self.gameStatus = 2

    def playCard(self, index):
        self.currentCard = cardIndex[index]
        horse_to_update = ""
        if ("C" in self.currentCard):
            horse_to_update = "AC"
        elif ("D" in self.currentCard):
            horse_to_update = "AD"
        elif ("H" in self.currentCard):
            horse_to_update = "AH"
        elif ("S" in self.currentCard):
            horse_to_update = "AS"        
        self.horses[horse_to_update]['position'] = self.horses[horse_to_update]['position'] + 1
        if (self.horses[horse_to_update]['position'] > (self.settings['trackLength'] + 1)):
            print('winner')
        self.usedCards.append(index)
    
    def getJSON(self):
        return self.__dict__
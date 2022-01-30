import random
import string

def generateRandomRoomID(length = 5):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))
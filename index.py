from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import json

# MODELS
from models.user import User
from models.room import Room
from utility import generateRandomRoomID

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# @app.route('/')
# def index():
#     return render_template('index.html',**values)

rooms = {}

@socketio.on('connect')
def test_connect():
    print('connected baby')
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('create_room')
def create_room(host_user):
    print("IN CREATE ROOM")
    roomID = generateRandomRoomID()
    while (roomID in rooms.keys()):
        roomID = generateRandomRoomID()
    join_room(roomID)
    user = User(host_user['username'], roomID, host_user['winnings'], 'host')
    room = Room(roomID, host_user['username'], user)
    rooms[roomID] = room
    emit('room_update',
        room.getJSON()
    , broadcast=True)

@socketio.on('join_room')
def join_the_room(roomID, player):
    if (roomID in rooms.keys()) and (len(player['username']) > 0):
        room = rooms[roomID]
        join_room(roomID)
        if (not player['username'] in room.players.keys()):
            user = User(player['username'], roomID, player['winnings'], 'player')
            room.addPlayer(user)
        emit('room_update',
            room.getJSON()
        , broadcast=True)

@socketio.on('leave_room')
def leave_the_room(roomID, player):
    if (roomID in rooms.keys()) and (len(player['username']) > 0):
        room = rooms[roomID]
        leave_room(roomID)
        room.removePlayer(player)
        emit('room_update',
            room.getJSON()
        , broadcast=True)

@socketio.on('start_betting')
def start_betting(roomID):
    if (roomID in rooms.keys()):
        room = rooms[roomID]
        room.randomizePlayerOrder()
        emit('room_update',
            room.getJSON()
        , broadcast=True)

@socketio.on('place_bet')
def start_betting(roomID, player, horse_id, wager, horse_name):
    if (roomID in rooms.keys()):
        room = rooms[roomID]
        room.placeBet(horse_id, player, wager, horse_name)
        room.changeBetTurn()
        if (room.currentIndex == len(room.playerOrder)):
            room.startGame()
        emit('room_update',
            room.getJSON()
        , broadcast=True)

@socketio.on('play_card')
def start_betting(roomID, index):
    if (roomID in rooms.keys()):
        room = rooms[roomID]
        room.playCard(index)
        emit('room_update',
            room.getJSON()
        , broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
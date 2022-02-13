import socket
import pickle
import sys

class User:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.inGame - False

class Game:
    def __init__(self):
        self.dealer = User()
        self.players = []

print('0')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('1')
sock.connect(('10.120.70.106', 12000))
print('connected')

#sock.setblocking(0)

while True:
    input = sys.stdin.readline()
    params = input.split(" ")
    if params[0] == 'register':
        sock.send(input.encode())
        ack = sock.recv(1024)
        print(ack)

    elif params[0] == 'query':
        if params[1] == 'players\n':
            sock.send(input.encode())
            ack = sock.recv(1024).decode()
            print(ack)
            for i in range(int(ack)):
                player = pickle.loads(sock.recv(2048))
                print('(', player.username, ',', player.ip, ',', player.port, ')')
                sock.send(b'ACK')
        
        elif params[1] == 'games\n':
            sock.send(input.encode())
            numGames = sock.recv(1024).decode()
            print('Number of active games:', numGames)
            for i in range(int(numGames)):
                game = pickle.loads(sock.recv(2048))
                print('Game', i, ':')
                print(game.dealer.username, game.dealer.ip, game.dealer.port)
                for player in game.players:
                    print(player.username, player.ip, player.port)
                sock.send(b'ACK')

    elif params[0] == 'start':
        sock.send(input.encode())
        ack = sock.recv(1024).decode()
        print(ack)

    elif params[0] == 'deregister':
        sock.send(input.encode())
        ack = sock.recv(1024).decode()
        print(ack)
        if ack == 'SUCCESS':
            sock.close()
    else:
        print("Invalid command")

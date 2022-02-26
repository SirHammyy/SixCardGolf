import socket
import pickle
import select
import sys

class User:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.inGame = False

class Game:
    def __init__(self):
        self.dealer = User()
        self.players = []

class Card:
    def __init__(self, value):
        self.value = value

class Deck:
    def __init__(self):
        self.cards = []

managerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
managerSock.connect(('localhost', 12000))

read_list = [managerSock, sys.stdin]
inGame = False
currentPlayers = []

#Loop forever
while True:
    readable, writable, errored = select.select(read_list, [], [], .5)
    #print('waiting')

    #Await for any messages
    for s in readable:
        if s is managerSock or mySock:
            data = s.recv(1024).decode()
            if data:
                s.send(b'ACK')
            print(data)
        else:                   #new input is from stdin
            params = input.split(" ")
            if params[0] == 'register':
                managerSock.send(input.encode())
                ack = managerSock.recv(1024).decode()
                print(ack)
                if ack == 'SUCCESS':
                    mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    mySock.bind(('', int(params[3])))
                    mySock.listen()
                    read_list.append(mySock)

            elif params[0] == 'query':
                if params[1] == 'players\n':
                    managerSock.send(input.encode())
                    ack = managerSock.recv(1024).decode()
                    print(ack)
                    for i in range(int(ack)):
                        player = pickle.loads(managerSock.recv(2048))
                        print('(', player.username, ',', player.ip, ',', player.port, ')')
                        managerSock.send(b'ACK')
                
                elif params[1] == 'games\n':
                    managerSock.send(input.encode())
                    numGames = managerSock.recv(1024).decode()
                    print('Number of active games:', numGames)
                    for i in range(int(numGames)):
                        game = pickle.loads(managerSock.recv(2048))
                        print('Game', i, ':')
                        print(game.dealer.username, game.dealer.ip, game.dealer.port)
                        for player in game.players:
                            print(player.username, player.ip, player.port)
                        managerSock.send(b'ACK')

            elif params[0] == 'start':
                managerSock.send(input.encode())
                status = managerSock.recv(1024).decode()
                if status == 'SUCCESS':
                    print(status)
                    dealer = pickle.loads(managerSock.recv(4096))
                    print('Dealer:', '(', dealer.username, dealer.ip, dealer.port, ')')
                    managerSock.send(b'ACK')
                    for i in range(int(params[3])):
                        currentPlayers.append(pickle.loads(managerSock.recv(4096)))
                        managerSock.send(b'ACK')
                    for i in range(len(currentPlayers)):
                        print('(', currentPlayers[i].username, currentPlayers[i].ip, currentPlayers[i].port, ')')
                        playerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        playerSocket.connect((currentPlayers[i].ip, int(currentPlayers[i].port)))
                        playerSocket.send(b'NEW GAME STARTED')

                else:
                    print(status)

            elif params[0] == 'deregister':
                managerSock.send(input.encode())
                ack = managerSock.recv(1024).decode()
                print(ack)
                if ack == 'SUCCESS':
                    managerSock.close()
            else:
                print("Invalid command")


    for w in writable:
        data = w.recv(1024).decode()
        print(data)
    for e in errored:
        print(e)

    #Handle player input
    # input = sys.stdin.readline()
    # params = input.split(" ")
    # if params[0] == 'register':
    #     managerSock.send(input.encode())
    #     ack = managerSock.recv(1024).decode()
    #     print(ack)
    #     if ack == 'SUCCESS':
    #         mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         mySock.bind(('', int(params[3])))
    #         mySock.listen()
    #         read_list.append(mySock)

    # elif params[0] == 'query':
    #     if params[1] == 'players\n':
    #         managerSock.send(input.encode())
    #         ack = managerSock.recv(1024).decode()
    #         print(ack)
    #         for i in range(int(ack)):
    #             player = pickle.loads(managerSock.recv(2048))
    #             print('(', player.username, ',', player.ip, ',', player.port, ')')
    #             managerSock.send(b'ACK')
        
    #     elif params[1] == 'games\n':
    #         managerSock.send(input.encode())
    #         numGames = managerSock.recv(1024).decode()
    #         print('Number of active games:', numGames)
    #         for i in range(int(numGames)):
    #             game = pickle.loads(managerSock.recv(2048))
    #             print('Game', i, ':')
    #             print(game.dealer.username, game.dealer.ip, game.dealer.port)
    #             for player in game.players:
    #                 print(player.username, player.ip, player.port)
    #             managerSock.send(b'ACK')

    # elif params[0] == 'start':
    #     managerSock.send(input.encode())
    #     status = managerSock.recv(1024).decode()
    #     if status == 'SUCCESS':
    #         print(status)
    #         dealer = pickle.loads(managerSock.recv(4096))
    #         print('Dealer:', '(', dealer.username, dealer.ip, dealer.port, ')')
    #         managerSock.send(b'ACK')
    #         for i in range(int(params[3])):
    #             currentPlayers.append(pickle.loads(managerSock.recv(4096)))
    #             managerSock.send(b'ACK')
    #         for i in range(len(currentPlayers)):
    #             print('(', currentPlayers[i].username, currentPlayers[i].ip, currentPlayers[i].port, ')')
    #             playerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             playerSocket.connect((currentPlayers[i].ip, int(currentPlayers[i].port)))
    #             playerSocket.send(b'NEW GAME STARTED')

    #     else:
    #         print(status)

    # elif params[0] == 'deregister':
    #     managerSock.send(input.encode())
    #     ack = managerSock.recv(1024).decode()
    #     print(ack)
    #     if ack == 'SUCCESS':
    #         managerSock.close()
    # else:
    #     print("Invalid command")
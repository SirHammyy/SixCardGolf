import socket
import pickle
import select

HOST = ''
PORT = 12000

class User:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.inGame = False
        self.hand = []
        self.score = 0

class Game:
    def __init__(self, dealer):
        self.dealer = dealer
        self.players = []
        self.id = 0
        self.deck = Deck()
        discard = []

class Card:
    def __init__(self, value):
        self.value = value

class Deck:
    def __init__(self):
        self.cards = [Card(' AS'), Card(' 2S'), Card(' 3S'), Card(' 4S'), Card(' 5S'), Card(' 6S'), Card(' 7S'), Card(' 8S'), Card(' 9S'), Card('10S'), Card(' JS'), Card(' QS'), Card(' KS'),
                    Card(' AC'), Card(' 2C'), Card(' 3C'), Card(' 4C'), Card(' 5C'), Card(' 6C'), Card(' 7C'), Card(' 8C'), Card(' 9C'), Card('10C'), Card(' JC'), Card(' QC'), Card(' KC'),
                    Card(' AH'), Card(' 2H'), Card(' 3H'), Card(' 4H'), Card(' 5H'), Card(' 6H'), Card(' 7H'), Card(' 8H'), Card(' 9H'), Card('10H'), Card(' JH'), Card(' QH'), Card(' KH'),
                    Card(' AD'), Card(' 2D'), Card(' 3D'), Card(' 4D'), Card(' 5D'), Card(' 6D'), Card(' 7D'), Card(' 8D'), Card(' 9D'), Card('10D'), Card(' JD'), Card(' QD'), Card(' KD'),
                    ]

activePlayers = []
availablePlayers = []
activeGames = []



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    read_list = [sock]
    print('Listening for players on port', PORT)
    while True:
        readable, writable, errored = select.select(read_list, [], [], .5)
        for s in readable:
            if s is sock:
                clientSocket, addr = sock.accept()
                read_list.append(clientSocket)
                print ("Connection from ", addr)
            else:
                data = s.recv(1024)
                params = data.decode().split(" ")
                if data:
                    print(data)
                    if params[0] == 'register':
                        username = params[1].replace(' ', '')
                        ip = params[2].replace(' ', '')
                        port = params[3].replace('\n', '')
                        unique = True
                        for i in activePlayers:
                            if i.username == username:
                                s.send(b'FAILURE')
                                unique = False
                                break
                            elif i.port == port:
                                s.send(b'FAILURE')
                                unique = False
                                break
                        
                        if unique:
                            s.send(b'SUCCESS')
                            tempUser = User(username, ip, port)
                            activePlayers.append(tempUser)
                            availablePlayers.append(tempUser)

                    elif params[0] == 'query':
                        if params[1] == 'players\n':
                            s.send(str(len(activePlayers)).encode())
                            for i in range(len(activePlayers)):
                                s.send(pickle.dumps(activePlayers[i]))
                                s.recv(1024)
                        
                        elif params[1] == 'games\n':
                            s.send(str(len(activeGames)).encode())
                            for i in range(len(activeGames)):
                                s.send(pickle.dumps(activeGames[i]))
                                s.recv(1024)


                    elif params[0] == 'start':
                        dealerInput = params[2]
                        playerCount = int(params[3].replace('\n', ''))
                        gameDealer = User("", "", "")
                        success = False

                        foundDealer = False
                        for i in availablePlayers:
                            if i.username == dealerInput:
                                foundDealer = True
                                gameDealer = i
                        
                        if not foundDealer:
                            success = False

                        elif len(availablePlayers) - 1 < int(params[3]):
                            success = False
                        
                        elif playerCount < 2 or playerCount > 4:
                            success = False

                        else:
                            success = True

                        if success:
                            s.send(b'SUCCESS')
                            newGame = Game(gameDealer)
                            newGame.id = len(activeGames)
                            s.send(pickle.dumps(gameDealer))
                            s.recv(1024)
                            s.send(str(newGame.id).encode())
                            s.recv(1024)
                            availablePlayers.remove(gameDealer)
                            for i in range(int(params[3])):
                                s.send(pickle.dumps(availablePlayers.pop()))
                                if i in availablePlayers:
                                    availablePlayers.remove(i)
                                s.recv(1024)

                            activeGames.append(newGame)
                        else:
                            s.send(b'FAILURE')

                    elif params[0] == 'end':
                        deletedGame = Game(User('temp','',''))
                        for i in activeGames:
                            if i.id == params[1] and i.dealer.username == params[2]:
                                deletedGame = i
                        
                        if deletedGame.dealer.username == 'temp':
                            s.send(b'FAILURE')
                        else:
                            activeGames.remove(deletedGame)
                            s.send(b'SUCCESS')


                    elif params[0] == 'deregister':
                        user = params[1].replace('\n', '')
                        foundPlayer = False
                        for i in activePlayers:
                            if i.username == user:
                                activePlayers.remove(i)
                                availablePlayers.remove(i)
                                s.send(b'SUCCESS')
                                
                                foundPlayer = True
                                break

                        if not foundPlayer:
                            s.send(b'FAILURE')

    

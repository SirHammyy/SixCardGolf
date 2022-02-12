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
    username = ""

class Game:
    def __init__(self, dealer):
        self.dealer = dealer
        self.players = []

activePlayers = []
activeGames = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    read_list = [sock]
    while True:
        readable, writable, errored = select.select(read_list, [], [])
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
                        for i in activePlayers:
                            if i.username == dealerInput:
                                foundDealer = True
                                gameDealer = i
                        
                        if not foundDealer:
                            success = False

                        elif len(activePlayers) - 1 < int(params[3]):
                            success = False
                        
                        elif playerCount < 2 or playerCount > 4:
                            success = False

                        else:
                            success = True

                        if success:
                            newGame = Game(gameDealer)
                            activeGames.append(newGame)
                            s.send(b'SUCCESS')
                        else:
                            s.send(b'FAILURE')


                    elif params[0] == 'deregister':
                        user = params[1].replace('\n', '')
                        foundPlayer = False
                        for i in activePlayers:
                            if i.username == user:
                                activePlayers.remove(i)
                                s.send(b'SUCCESS')
                                
                                foundPlayer = True
                                break

                        if not foundPlayer:
                            s.send(b'FAILURE')
                            

                    else:
                        print("Player left")
                        read_list.remove(s)

    
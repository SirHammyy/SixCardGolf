from re import L
import socket
import pickle
import select
import sys
import random

class User:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.inGame = False
        self.hand = []
        self.score = 0

class Game:
    def __init__(self):
        self.dealer = any
        self.players = []
        self.id = 0
        self.deck = Deck()
        self.discard = []

class Card:
    def __init__(self, value):
        self.value = value
        self.revealed = False

class Deck:
    def __init__(self):
        self.cards = [Card(' AS'), Card(' 2S'), Card(' 3S'), Card(' 4S'), Card(' 5S'), Card(' 6S'), Card(' 7S'), Card(' 8S'), Card(' 9S'), Card('10S'), Card(' JS'), Card(' QS'), Card(' KS'),
                    Card(' AC'), Card(' 2C'), Card(' 3C'), Card(' 4C'), Card(' 5C'), Card(' 6C'), Card(' 7C'), Card(' 8C'), Card(' 9C'), Card('10C'), Card(' JC'), Card(' QC'), Card(' KC'),
                    Card(' AH'), Card(' 2H'), Card(' 3H'), Card(' 4H'), Card(' 5H'), Card(' 6H'), Card(' 7H'), Card(' 8H'), Card(' 9H'), Card('10H'), Card(' JH'), Card(' QH'), Card(' KH'),
                    Card(' AD'), Card(' 2D'), Card(' 3D'), Card(' 4D'), Card(' 5D'), Card(' 6D'), Card(' 7D'), Card(' 8D'), Card(' 9D'), Card('10D'), Card(' JD'), Card(' QD'), Card(' KD'),
                    ]

def ShuffleDeck(deck):
    newOrder = []
    for i in range(52):
        randomPos = random.randrange(0, len(deck.cards))
        newOrder.append(deck.cards[randomPos])
        deck.cards.remove(deck.cards[randomPos])

    newDeck = Deck()
    newDeck.cards = newOrder
    return newDeck



def SendCards(currentPlayer):
    peerSock.sendto(b'HANDS', (currentPlayer.ip, int(currentPlayer.port)))
    playerHand = ""

    if currentPlayer.hand[0].revealed:
        playerHand = playerHand + currentPlayer.hand[0].value + ' '
    else:
        playerHand = playerHand + "*** "

    if currentPlayer.hand[2].revealed:
        playerHand = playerHand + currentPlayer.hand[2].value + ' '
    else:
        playerHand = playerHand + "*** "
    
    if currentPlayer.hand[4].revealed:
        playerHand = playerHand + currentPlayer.hand[4].value + '\n'
    else:
        playerHand = playerHand + "*** " + '\n'

    if currentPlayer.hand[1].revealed:
        playerHand = playerHand + currentPlayer.hand[1].value + ' '
    else:
        playerHand = playerHand + "*** "

    if currentPlayer.hand[3].revealed:
        playerHand = playerHand + currentPlayer.hand[3].value + ' '
    else:
        playerHand = playerHand + "*** "

    if currentPlayer.hand[5].revealed:
        playerHand = playerHand + currentPlayer.hand[5].value + ' '
    else:
        playerHand = playerHand + "*** "

    peerSock.sendto(playerHand.encode(), (currentPlayer.ip, int(currentPlayer.port)))

    for player in currentGame.players:
        if player != currentPlayer:
            hand = ""

            if player.hand[0].revealed:
                hand = hand + player.hand[0].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[2].revealed:
                hand = hand + player.hand[2].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[4].revealed:
                hand = hand + player.hand[4].value + '\n'
            else:
                hand = hand + "*** " + '\n'

            if player.hand[1].revealed:
                hand = hand + player.hand[1].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[3].revealed:
                hand = hand + player.hand[3].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[5].revealed:
                hand = hand + player.hand[5].value + ' '
            else:
                hand = hand + "*** "

            peerSock.sendto(player.username.encode(), (currentPlayer.ip, int(currentPlayer.port)))
            peerSock.sendto(hand.encode(), (currentPlayer.ip, int(currentPlayer.port)))

    peerSock.sendto(currentGame.deck.cards[len(currentGame.deck.cards) - 1].value.encode(), (currentPlayer.ip, int(currentPlayer.port)))
    if len(currentGame.discard) == 0:
        peerSock.sendto("***".encode(), (currentPlayer.ip, int(currentPlayer.port)))
    else:
        peerSock.sendto(currentGame.discard[len(currentGame.discard) - 1].value.encode(), (currentPlayer.ip, int(currentPlayer.port)))

def PrintCards(currentPlayer):
    print('HANDS')
    playerHand = ""

    if currentPlayer.hand[0].revealed:
        playerHand = playerHand + currentPlayer.hand[0].value + ' '
    else:
        playerHand = playerHand + "*** "

    if currentPlayer.hand[2].revealed:
        playerHand = playerHand + currentPlayer.hand[2].value + ' '
    else:
        playerHand = playerHand + "*** "
    
    if currentPlayer.hand[4].revealed:
        playerHand = playerHand + currentPlayer.hand[4].value + '\n'
    else:
        playerHand = playerHand + "*** " + '\n'

    if currentPlayer.hand[1].revealed:
        playerHand = playerHand + currentPlayer.hand[1].value + ' '
    else:
        playerHand = playerHand + "*** "

    if currentPlayer.hand[3].revealed:
        playerHand = playerHand + currentPlayer.hand[3].value + ' '
    else:
        playerHand = playerHand + "*** "

    if currentPlayer.hand[5].revealed:
        playerHand = playerHand + currentPlayer.hand[5].value + ' '
    else:
        playerHand = playerHand + "*** "

    print('Your hand:')
    print(playerHand + '\n')

    for player in currentGame.players:
        if player != currentPlayer:
            hand = ""

            if player.hand[0].revealed:
                hand = hand + player.hand[0].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[2].revealed:
                hand = hand + player.hand[2].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[4].revealed:
                hand = hand + player.hand[4].value + '\n'
            else:
                hand = hand + "*** " + '\n'

            if player.hand[1].revealed:
                hand = hand + player.hand[1].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[3].revealed:
                hand = hand + player.hand[3].value + ' '
            else:
                hand = hand + "*** "

            if player.hand[5].revealed:
                hand = hand + player.hand[5].value + ' '
            else:
                hand = hand + "*** "

            print(player.username + "'s hand:")
            print(hand + '\n')

    print('Draw pile: ***')
    if len(currentGame.discard) == 0:
        print('Discard: ***')
    else:
        print('Discard: ' + currentGame.discard[len(currentGame.discard) - 1].value)



    
def SendHand(player):
    playerHand = ""

    if player.hand[0].revealed:
        playerHand = playerHand + player.hand[0].value + ' '
    else:
        playerHand = playerHand + "*** "

    if player.hand[2].revealed:
        playerHand = playerHand + player.hand[2].value + ' '
    else:
        playerHand = playerHand + "*** "
    
    if player.hand[4].revealed:
        playerHand = playerHand + player.hand[4].value + '\n'
    else:
        playerHand = playerHand + "*** " + '\n'

    if player.hand[1].revealed:
        playerHand = playerHand + player.hand[1].value + ' '
    else:
        playerHand = playerHand + "*** "

    if player.hand[3].revealed:
        playerHand = playerHand + player.hand[3].value + ' '
    else:
        playerHand = playerHand + "*** "

    if player.hand[5].revealed:
        playerHand = playerHand + player.hand[5].value + ' '
    else:
        playerHand = playerHand + "*** "

    peerSock.sendto(playerHand.encode(), (player.ip, int(player.port)))

def PrintHand(player):
    playerHand = ""
    
    if player.hand[0].revealed:
        playerHand = playerHand + player.hand[0].value + ' '
    else:
        playerHand = playerHand + "*** "

    if player.hand[2].revealed:
        playerHand = playerHand + player.hand[2].value + ' '
    else:
        playerHand = playerHand + "*** "
    
    if player.hand[4].revealed:
        playerHand = playerHand + player.hand[4].value + ' \n'
    else:
        playerHand = playerHand + "*** " + '\n'

    if player.hand[1].revealed:
        playerHand = playerHand + player.hand[1].value + ' '
    else:
        playerHand = playerHand + "*** "

    if player.hand[3].revealed:
        playerHand = playerHand + player.hand[3].value + ' '
    else:
        playerHand = playerHand + "*** "

    if player.hand[5].revealed:
        playerHand = playerHand + player.hand[5].value + ' '
    else:
        playerHand = playerHand + "*** "
    
    print(playerHand)

def CheckDuplicates(player, pos):
    newCard = player.hand[pos]
    for i in reversed(range(pos)):
        if player.hand[i].value[0] == newCard.value[0] and player.hand[i].value[1] == newCard.value[1]:
            if i % 2 == 0:
                player.hand[pos] = player.hand[i + 1]
                player.hand[i + 1] = newCard
            else:
                player.hand[pos] = player.hand[i - 1]
                player.hand[i - 1] = newCard
            break


def AddScores():
    for currentPlayer in currentGame.players:
        for i in range(6):
            if i % 2 == 0 and currentPlayer.hand[i].value[0] == currentPlayer.hand[i + 1].value[0] and currentPlayer.hand[i].value[1] == currentPlayer.hand[i + 1].value[1]:
                continue
            elif i % 2 == 1 and currentPlayer.hand[i].value[0] == currentPlayer.hand[i - 1].value[0] and currentPlayer.hand[i].value[1] == currentPlayer.hand[i - 1].value[1]:
                continue
            else:
                if currentPlayer.hand[i].value[1] == '2':
                    currentPlayer.score = currentPlayer.score - 2
                elif currentPlayer.hand[i].value[1] == 'A':
                    currentPlayer.score = currentPlayer.score + 1
                elif currentPlayer.hand[i].value[1] == 'J' or currentPlayer.hand[i].value[1] == 'Q':
                    currentPlayer.score = currentPlayer.score + 10
                elif currentPlayer.hand[i].value[1] == 'K':
                    currentPlayer.score = currentPlayer.score + 0
                elif currentPlayer.hand[i].value[0] == '1':
                    currentPlayer.score = currentPlayer.score + 10
                else:
                    currentPlayer.score = currentPlayer.score + int(currentPlayer.hand[i].value[1])




def StartGameLoop():
    print('Number of players:',len(currentGame.players))

    #Play 9 holes
    for hole in range(9):
        #Shuffle new deck
        currentGame.deck = ShuffleDeck(currentGame.deck)

        #Deal cards
        for currentPlayer in currentGame.players:
            for i in range(6):
                currentPlayer.hand.append(currentGame.deck.cards.pop())

            currentPlayer.hand[0].revealed = True
            currentPlayer.hand[1].revealed = True

        currentGame.discard.append(currentGame.deck.cards.pop())

        #Initiate everyone for current hole
        for currentPlayer in currentGame.players:
            if currentPlayer != currentGame.dealer:
                msg = 'STARTING HOLE ' + str(hole + 1)
                peerSock.sendto(msg.encode(), (currentPlayer.ip, int(currentPlayer.port)))
                peerSock.sendto(pickle.dumps(currentGame), (currentPlayer.ip, int(currentPlayer.port)))
            else:
                print('STARTING HOLE ' + str(hole + 1) + '\n')

        #Start game loop for current hole
        currentCard = 2
        while currentCard < 6:
            for currentPlayer in currentGame.players:
                if currentPlayer != currentGame.dealer:
                    SendCards(currentPlayer)
                    peerSock.sendto(b'WAITING FOR MOVE', (currentPlayer.ip, int(currentPlayer.port)))
                    move, addr = peerSock.recvfrom(1024)
                    move = move.decode().replace('\n', '').lower()
                    print(currentPlayer.username + "'s move: " + move)
                    moveParams = move.split(' ')

                    #Compute player's move
                    if moveParams[0] == "draw":
                        newCard = Card("")
                        if moveParams[1] == "discard":
                            #Draw discard
                            newCard = currentGame.discard.pop()
                            currentGame.discard.append(currentPlayer.hand[currentCard])
                            currentPlayer.hand[currentCard] = newCard
                            currentPlayer.hand[currentCard].revealed = True
                            CheckDuplicates(currentPlayer, currentCard)
                            SendHand(currentPlayer)
                        elif moveParams[1] == "pile":
                            #Draw from draw pile
                            newCard = currentGame.deck.cards.pop()
                            currentGame.discard.append(currentPlayer.hand[currentCard])
                            currentPlayer.hand[currentCard] = newCard
                            currentPlayer.hand[currentCard].revealed = True
                            CheckDuplicates(currentPlayer, currentCard)
                            SendHand(currentPlayer)
                    
                    elif moveParams[0] == "steal":
                        stolenUser = User('temp','','')
                        stolenCardInput = moveParams[2].replace('\n', '')
                        if len(stolenCardInput) == 2:
                            stolenCardInput = ' ' + stolenCardInput
                        #Stealing from other player
                        if moveParams[1] != currentGame.dealer.username:
                            for i in currentGame.players:
                                if i.username.lower() == moveParams[1].lower():
                                    stolenUser = i
                            stolenCard = Card('')
                            replacedCard = currentPlayer.hand[currentCard]
                            for i in range(len(stolenUser.hand)):
                                if stolenUser.hand[i].value.lower() == stolenCardInput.lower():
                                    stolenCard = stolenUser.hand[i]
                                    stolenUser.hand[i] = replacedCard
                                    stolenUser.hand[i].revealed = True
                            
                            currentPlayer.hand[currentCard] = stolenCard
                            currentPlayer.hand[currentCard].revealed = True
                            CheckDuplicates(currentPlayer, currentCard)
                            CheckDuplicates(stolenUser, currentCard)
                            SendHand(stolenUser)
                            SendHand(currentPlayer)
                            
                        
                        #Stealing from dealer
                        else:
                            stolenUser = User('temp','','')
                            for i in currentGame.players:
                                if i.username.lower() == currentGame.dealer.username.lower():
                                    stolenUser = i
                            print('STEALING')
                            
                            stolenCard = Card('')
                            stolenCardPos = 0
                            replacedCard = currentPlayer.hand[currentCard]
                            for i in range(len(stolenUser.hand)):
                                if stolenUser.hand[i].value.lower() == stolenCardInput.lower():
                                    stolenCardPos = i
                                    stolenCard = stolenUser.hand[i]
                                    stolenUser.hand[i] = replacedCard
                                    stolenUser.hand[i].revealed = True
                            currentPlayer.hand[currentCard] = stolenCard
                            currentPlayer.hand[currentCard].revealed = True
                            CheckDuplicates(currentPlayer, currentCard)
                            CheckDuplicates(stolenUser, stolenCardPos)
                            SendHand(currentPlayer)
                            print('New Hand:')
                            PrintHand(stolenUser)

                        


                #Basically do what you do for other players, but for yourself
                elif currentPlayer.username == currentGame.dealer.username:
                    PrintCards(currentPlayer)
                    print('WAITING FOR MOVE')
                    move = sys.stdin.readline()
                    move = move.replace('\n', '').lower()
                    print(currentPlayer.username + "'s move: " + move)
                    moveParams = move.split(' ')

                    #Compute player's move
                    if moveParams[0] == "draw":
                        newCard = Card("")
                        if moveParams[1] == "discard":
                            #Draw discard
                            newCard = currentGame.discard.pop()
                            currentGame.discard.append(currentPlayer.hand[currentCard])
                            currentPlayer.hand[currentCard] = newCard
                            currentPlayer.hand[currentCard].revealed = True
                            CheckDuplicates(currentPlayer, currentCard)
                            print('New hand:')
                            PrintHand(currentPlayer)
                        elif moveParams[1] == "pile":
                            #Draw from draw pile
                            newCard = currentGame.deck.cards.pop()
                            currentGame.discard.append(currentPlayer.hand[currentCard])
                            currentPlayer.hand[currentCard] = newCard
                            currentPlayer.hand[currentCard].revealed = True
                            CheckDuplicates(currentPlayer, currentCard)
                            print('New hand:')
                            PrintHand(currentPlayer)

                    elif moveParams[0] == "steal":
                        stolenUser = User('temp','','')
                        stolenCardInput = moveParams[2].replace('\n', '')
                        if len(stolenCardInput) == 2:
                            stolenCardInput = ' ' + stolenCardInput
                        for i in currentGame.players:
                            if i.username.lower() == moveParams[1].lower():
                                stolenUser = i
                        peerSock.sendto(b'STEALING', (stolenUser.ip, int(stolenUser.port)))
                        stolenCard = Card('')
                        stolenCardPos = 0
                        replacedCard = currentPlayer.hand[currentCard]
                        for i in range(len(stolenUser.hand)):
                            if stolenUser.hand[i].value.lower() == stolenCardInput.lower():
                                stolenCardPos = i
                                stolenCard = stolenUser.hand[i]
                                stolenUser.hand[i] = replacedCard
                                stolenUser.hand[i].revealed = True
                        currentPlayer.hand[currentCard] = stolenCard
                        currentPlayer.hand[currentCard].revealed = True
                        CheckDuplicates(currentPlayer, currentCard)
                        CheckDuplicates(stolenUser, stolenCardPos)
                        SendHand(stolenUser)
                        print('New Hand:')
                        PrintHand(currentPlayer)
                        print('')

            currentCard = currentCard + 1

        AddScores()


        #Send updated scores to each player
        for currentPlayer in currentGame.players:
            if currentPlayer != currentGame.dealer:
                peerSock.sendto(b'UPDATED SCORES', (currentPlayer.ip, int(currentPlayer.port)))
                peerSock.sendto(str(hole + 1).encode(), (currentPlayer.ip, int(currentPlayer.port)))
                for playerScore in currentGame.players:
                    peerSock.sendto(playerScore.username.encode(), (currentPlayer.ip, int(currentPlayer.port)))
                    peerSock.sendto(str(playerScore.score).encode(), (currentPlayer.ip, int(currentPlayer.port)))

        #Also print them here at dealer
        print("\nScores after hole " + str(hole + 1) + ":")
        for currentPlayer in currentGame.players:
            print(currentPlayer.username + ": " + str(currentPlayer.score))

        for currentPlayer in currentGame.players:
            currentPlayer.hand.clear()

        currentGame.deck = Deck()
        currentGame.discard.clear()





managerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
managerSock.connect(('localhost', 12000))
mySock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
peerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
read_list = [managerSock, sys.stdin]
inGame = False
isDealer = False
currentGame = Game()

#Loop forever
while True:
    readable, writable, errored = select.select(read_list, [], [], .5)

    #Await for any messages
    for s in readable:
        if s is mySock:                           #new input is from socket
            data, addr = s.recvfrom(1024)
            data = data.decode()
            print(data)

            #Recieved notif for joining a new game
            if data == 'NEW GAME STARTED':
                s.sendto(b'ACK', addr)
                data, addr = s.recvfrom(2048)
                currentGame = pickle.loads(data)
                s.sendto(b'ACK', addr)

            #Get Players move
            elif data == 'WAITING FOR MOVE':
                move = sys.stdin.readline().lower().replace('\n', '')
                sentMove = move
                moveParams = move.split(' ')
                if moveParams[0] == 'draw':
                    if moveParams[1] == 'discard':
                        s.sendto(sentMove.encode(), addr)
                        moveData, moveAddr = s.recvfrom(1024)
                        print("New hand:")
                        print(moveData.decode())
                    elif moveParams[1] == 'pile':
                        s.sendto(sentMove.encode(), addr)
                        moveData, moveAddr = s.recvfrom(1024)
                        print("New hand:")
                        print(moveData.decode() + '\n')
                
                elif moveParams[0] == 'steal':
                    stolen = User('temp','','')
                    if moveParams[1] != currentGame.dealer.username:
                        for i in currentGame.players:
                            if i.username == moveParams[1]:
                                stolen = i
                        s.sendto(b'STEALING', (stolen.ip, int(stolen.port)))
                        s.sendto(sentMove.encode(), addr)
                        newHand, newHandAddr = s.recvfrom(1024)
                        print('New Hand:')
                        print(newHand.decode() + '\n')
                    else:
                        s.sendto(sentMove.encode(), addr)
                        newHand, newHandAddr = s.recvfrom(1024)
                        print('New Hand:')
                        print(newHand.decode() + '\n')


            #Displaying all current cards
            elif data == 'HANDS':
                #Print my cards
                data, addr = s.recvfrom(1024)
                data = data.decode()
                print('Your hand:')
                print(data + '\n')

                #Print every other player's cards
                for i in range(len(currentGame.players)):
                    data, addr = s.recvfrom(1024)
                    data = data.decode()
                    print(data + "'s hand:")
                    data, addr = s.recvfrom(1024)
                    data = data.decode()
                    print(data + '\n')
                
                #Print draw and discard piles
                deck, addr1 = s.recvfrom(1024)
                deck = deck.decode()
                discard, addr2 = s.recvfrom(1024)
                discard = discard.decode()
                print('Draw pile: ***')
                print('Discard: ' + discard + "\n")

            elif data[0] == 'S' and data[1] == 'T' and data[2] == 'A' and data[3] == 'R' and data[4] == 'T':
                print('')
                newGame, addrG = s.recvfrom(2048)
                currentGame = pickle.loads(newGame)
                currentGame.players.remove(currentGame.dealer)

            elif data == 'UPDATED SCORES':
                hole, addrHole = s.recvfrom(1024)
                print('\nScores after hole ' + str(hole.decode()))
                for i in range(len(currentGame.players) + 1):
                    currentUserName, addrC = s.recvfrom(1024)
                    score, addrScore = s.recvfrom(1024)
                    print(currentUserName.decode() + ": " + score.decode())
                print('\n')

            elif data == 'STEALING':
                newHand, newHandAddr = s.recvfrom(1024)
                print('New Hand:')
                print(newHand.decode() + '\n')

            else:
                s.sendto(data.encode(), addr)

        elif s == sys.stdin:
            input = sys.stdin.readline()       #new input is from stdin
            params = input.split(" ")

            #Handle server manager commands
            if params[0] == 'register':
                managerSock.send(input.encode())
                ack = managerSock.recv(1024).decode()
                print(ack)
                if ack == 'SUCCESS':
                    print(params[3].replace('\n', ''))
                    mySock.bind(('', int(params[3].replace('\n', ''))))
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
                        print('Game', game.id, ':')
                        print(game.dealer.username, game.dealer.ip, game.dealer.port)
                        for player in game.players:
                            print(player.username, player.ip, player.port)
                        managerSock.send(b'ACK')
                else:
                    print("Invalid command")

            elif params[0] == 'start':
                managerSock.send(input.encode())
                status = managerSock.recv(1024).decode()
                if status == 'SUCCESS':
                    print(status)
                    currentPlayers = []
                    currentGame = Game()
                    dealer = pickle.loads(managerSock.recv(4096))
                    print('Dealer:', '(', dealer.username, dealer.ip, dealer.port, ')')
                    managerSock.send(b'ACK')
                    currentGame.dealer = dealer
                    gameID = managerSock.recv(1024)
                    managerSock.send(b'ACK')
                    currentGame.id = gameID
                    print('Players:')
                    for i in range(int(params[3])):
                        currentPlayers.append(pickle.loads(managerSock.recv(4096)))
                        managerSock.send(b'ACK')
                    currentGame.players = currentPlayers

                    for i in range(len(currentPlayers)):
                        print('(', currentPlayers[i].username, currentPlayers[i].ip, currentPlayers[i].port, ')')
                        #peerSock.connect((currentPlayers[i].ip, int(currentPlayers[i].port)))
                        if peerSock not in read_list:
                            read_list.append(peerSock)
                        peerSock.sendto(b'NEW GAME STARTED', (str(currentPlayers[i].ip), int(currentPlayers[i].port)))
                        peerSock.recvfrom(1024)
                        peerSock.sendto(pickle.dumps(currentGame), (str(currentPlayers[i].ip), int(currentPlayers[i].port)))
                        peerSock.recvfrom(1024)
                    inGame = True
                    isDealer = True
                    currentGame.players.append(dealer)
                    StartGameLoop()


                else:
                    print(status)

            elif params[0] == 'deregister':
                managerSock.send(input.encode())
                ack = managerSock.recv(1024).decode()
                print(ack)
                if ack == 'SUCCESS':
                    managerSock.close()
                    read_list.remove(managerSock)


            else:
                print("Invalid command")

        else:
             print('Something came in')

    for w in writable:
        data = w.recv(1024).decode()
        print(data)
    for e in errored:
        print(e)
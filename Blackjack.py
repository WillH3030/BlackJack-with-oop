import random
import time
from os import system

# This Table class connects the dealer to the players and some game logic.
class Table:
    def __init__(self, startingPlayerNames):
        #Sets up the starting players.
        self.players = []
        for name in startingPlayerNames :
            self.players.append(Player(name))

        #Sets up the dealer
        self.dealer = Dealer()
        self.isDealerTurn = False

    def displayTable(self):
        clearScreen()
        self.printDealer()

         
        cardLines = ''
        for player in self.players:
            cardLines += player.getCardLine()
        print(cardLines)

        nameLines = ''
        for player in self.players:
            nameLines += player.getNameLine()
        print(nameLines)

        chipLines = ''
        for player in self.players:
            chipLines += player.getChipLine()
        print(chipLines)

        print('')

    def printDealer(self):
        offset = ' ' * (len(self.players) * 10 - 10)
        print(offset + '   .------\ /------.')
        print(offset + '   |       -       |')
        print(offset + '   |               |')
        print(offset + '   |               |')
        print(offset + '   |               |')
        print(offset + '_______________________')
        print(offset + '===========.===========')
        print(offset + '  / ~~~~~     ~~~~~ \\')
        print(offset + ' /| | 0 |     | 0 |  |\\')
        print(offset + ' W   ---  / \  ---    W')
        print(offset + ' \.      |o o|      ./')
        print(offset + '  |                 |')
        print(offset + '  \    #########    /')
        print(offset + '   \  ## ----- ##  /')
        print(offset + '    \##         ##/')
        print(offset + '     \_____v_____/')
        print()
        print(offset + '         DEALER')
        print(offset + self.dealer.getDealerLine(self.isDealerTurn))

    def evaluateRound(self):
        for player in self.players:
            if player.hand.handValue() > 21:
                if self.dealer.hand.handValue() > 21:
                    player.tie()
                else:
                    player.lose()
            else:
                if self.dealer.hand.handValue() > 21:
                    player.win()

                elif player.hand.handValue() > self.dealer.hand.handValue():
                    player.win()

                elif player.hand.handValue() == self.dealer.hand.handValue():
                    player.tie()
                else:
                    player.lose()
            player.hand.emptyHand()
            time.sleep(1)

        self.dealer.hand.emptyHand()

    def kickPlayer(self):
        for player in self.players:
            if player.chipCount == 0:
                print('Oh no ' + player.name + ', you are out.')
                self.players.remove(player)

# The Dealer Class manages the deck of cards and the AI for dealer play.
class Dealer:
    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()

    def deal(self, playersAtTable):
        self.deck.shuffle()
        for i in range(0, 2):
            self.hand.addCard(self.deck.distribute1Card())
            for player in playersAtTable:
                player.hand.addCard(self.deck.distribute1Card())

    def hit(self, player):
        player.hand.addCard(self.deck.distribute1Card())

    def getDealerLine(self, dealerTurn):
        if len(self.hand.cardsInHand) == 0:
            return ''
        if dealerTurn:
            return '         ' + ' '.join(self.hand.cardsInHand) + ' (' + str(self.hand.handValue()) + ')'
        else:
            return '         ' + self.hand.cardsInHand[0] + ' ??'

    def playTurn(self):
        while True:
            if self.hand.handValue() < 17:
                self.hand.addCard(self.deck.distribute1Card())
            else:
                break

# The Player class keeps track of a player's chips, bets, and hand. It also handles most interactions
# with the person playing the game.
class Player:
    displayLength = 20
    def __init__(self, name):
        self.name = name.strip()
        self.hand = Hand()
        self.chipCount = 100
        self.bet = 0

    def placeBet(self):
        while True:
            try:
                self.bet = int(input(self.name + ', how much is your bet? \n'))
                if self.chipCount - self.bet < 0:
                    print("That is too much you don't have enough chips.")
                else:
                    self.chipCount -= self.bet
                    break
            except:
                print('That is not a valid number')

    def getCardLine(self):
        if len(self.hand.cardsInHand) == 0:
            return self.addBlankSpace('Empty Hand')

        cardLine = ' '.join(self.hand.cardsInHand)
        cardLine +=  ' ('  + str(self.hand.handValue()) + ')'
        return self.addBlankSpace(cardLine)

    def getNameLine(self):
        nameLine = self.name + ' ' + str(self.bet)
        return self.addBlankSpace(nameLine)

    def getChipLine(self):
        chipLine = 'Total Chips: ' + str(self.chipCount)
        return self.addBlankSpace(chipLine)

    def addBlankSpace(self, line):
        space = ' '
        spaceMultiplier = 0
        if len(line) < self.displayLength:
            spaceMultiplier = self.displayLength - len(line)
        return line + (space * spaceMultiplier)

    def hitOrPass(self):
        #Hit is True, Pass is False
        response = input(self.name + ' would you like to HIT or PASS? \n')
        while True:
            if response.upper() == 'HIT':
                return True
            elif response.upper() == 'PASS':
                return False
            else:
                response = input("I did not understand that. Please try again, HIT or PASS? \n")

    def win(self):
        print('Congratulations ' + self.name + ', you win this hand.')
        self.chipCount += self.bet * 2
        self.bet = 0

    def lose(self):
        print('I"m sorry ' + self.name + ', you lost this hand.')
        self.bet = 0

    def tie(self):
        print('Well ' + self.name + ', we tie this hand.')
        self.chipCount += self.bet
        self.bet = 0

# The Deck class handles the functionality of the deck. Primarily reseting, shuffling, and taking cards from the deck.
class Deck:
    masterCardList = ['D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK', 'DA',
                 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK', 'HA',
                 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK', 'CA',
                 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK', 'SA']

    def __init__(self) :
        self.cards = self.masterCardList[:]

    def shuffle(self):
        self.cards = self.masterCardList[:]
        random.shuffle(self.cards)

    def distribute1Card(self):
        return self.cards.pop()

# The Hand class stores the cards the player has and has functionality to score the hand.
class Hand:
    def __init__(self):
        self.cardsInHand = []

    def addCard(self, newCard):
        self.cardsInHand.append(newCard)

    def emptyHand(self):
        del self.cardsInHand[:]

    def handValue(self):
        cardValues = {'D2' : 2, 'D3' : 3, 'D4' : 4, 'D5' : 5, 'D6' : 6, 'D7' : 7, 'D8' : 8, 'D9' : 9, 'D10' : 10, 'DJ' : 10, 'DQ' : 10, 'DK' : 10, 'DA' : 1,
         'H2' : 2, 'H3' : 3, 'H4' : 4, 'H5' : 5, 'H6' : 6, 'H7' : 7, 'H8' : 8, 'H9' : 9, 'H10' : 10, 'HJ' : 10, 'HQ' : 10, 'HK' : 10, 'HA' : 1,
         'C2' : 2, 'C3' : 3, 'C4' : 4, 'C5' : 5, 'C6' : 6, 'C7' : 7, 'C8' : 8, 'C9' : 9, 'C10' : 10, 'CJ' : 10, 'CQ' : 10, 'CK' : 10, 'CA' : 1,
         'S2' : 2, 'S3' : 3, 'S4' : 4, 'S5' : 5, 'S6' : 6, 'S7' : 7, 'S8' : 8, 'S9' : 9, 'S10' : 10, 'SJ' : 10, 'SQ' : 10, 'SK' : 10, 'SA' : 1}
        sum = 0
        aceCheck = False

        for card in self.cardsInHand :
            sum += cardValues.get(card, 0)
            if card[1] == 'A':
                aceCheck = True

        if aceCheck and sum <= 11:
            sum += 10
        return sum

def clearScreen():
    _ = system('cls')

def getPlayerNames():
    return input('Enter the player names in a comma separated list. (ex: Kathy, Jim Bo, Ken) \n').split(',')

def welcomePage():
    print('''
    $$$$$$$\  $$\                     $$\                $$$$$\                     $$\              $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  
    $$  __$$\ $$ |                    $$ |               \__$$ |                    $$ |            $$  __$$\ $$$ __$$\ $$  __$$\ $$$ __$$\ 
    $$ |  $$ |$$ | $$$$$$\   $$$$$$$\ $$ |  $$\             $$ | $$$$$$\   $$$$$$$\ $$ |  $$\       \__/  $$ |$$$$\ $$ |\__/  $$ |$$$$\ $$ |
    $$$$$$$\ |$$ | \____$$\ $$  _____|$$ | $$  |            $$ | \____$$\ $$  _____|$$ | $$  |       $$$$$$  |$$\$$\$$ | $$$$$$  |$$\$$\$$ |
    $$  __$$\ $$ | $$$$$$$ |$$ /      $$$$$$  /       $$\   $$ | $$$$$$$ |$$ /      $$$$$$  /       $$  ____/ $$ \$$$$ |$$  ____/ $$ \$$$$ |
    $$ |  $$ |$$ |$$  __$$ |$$ |      $$  _$$<        $$ |  $$ |$$  __$$ |$$ |      $$  _$$<        $$ |      $$ |\$$$ |$$ |      $$ |\$$$ |
    $$$$$$$  |$$ |\$$$$$$$ |\$$$$$$$\ $$ | \$$\       \$$$$$$  |\$$$$$$$ |\$$$$$$$\ $$ | \$$\       $$$$$$$$\ \$$$$$$  /$$$$$$$$\ \$$$$$$  /
    \_______/ \__| \_______| \_______|\__|  \__|       \______/  \_______| \_______|\__|  \__|      \________| \______/ \________| \______/ 
                                                                                                                                            
                                                                                                                                            
                                                    Type PLAY to begin or HELP for instructions                                             ''')

    response = input()
    while True :
        if response.upper() == 'PLAY' or response.upper() == 'HELP':
            return response.upper()
        else :
            print('how can you not follow simple instructions, the fuck is wrong with you. william is gay.')
            response = input('Try again \n')

def helpPage():
    clearScreen()
    print('OBJECT OF THE GAME \n Each participant attempts to beat the dealer by getting a count as close to 21 as possible, without going over 21. \n')
    print('SCORING \n It is up to each individual player if an ace is worth 1 or 11. Face cards are 10 and any other card is its pip value. \n')
    print('PLAY \n The player to the left goes first and must decide whether to "stand" (not ask for another card) or "hit" (ask for another card in an attempt to get closer to a count of 21, or even hit 21 exactly). Thus, a player may stand on the two cards originally dealt to them, or they may ask the dealer for additional cards, one at a time, until deciding to stand on the total (if it is 21 or under), or goes "bust" (if it is over 21). In the latter case, the player loses and the dealer collects the bet wagered. The dealer then turns to the next player to their left and serves them in the same manner. \n')
    input('Press enter when you are ready to begin. \n \n \n')

def playGame():
    #Initialization
    playing = True
    clearScreen()
    table = Table(getPlayerNames())

    # Executes the game in the order of
    # 1) getting bets
    # 2) dealing cards
    # 3) players going through turns
    # 4) dealer playing
    # 5) awarding hands
    # 6) presenting the option to quit or keep playing

    while playing :
        #Bets
        for player in table.players:
            table.displayTable()
            player.placeBet()

        #Dealing
        table.isDealerTurn = False
        table.dealer.deal(table.players)

        #Players playing
        for player in table.players:
            while True:
                table.displayTable()
                if player.hand.handValue() > 21:
                    print('Oh no you busted!')
                    time.sleep(1.5)
                    break
                elif player.hitOrPass():
                    table.dealer.hit(player)
                else:
                    break

        #Dealer Turn
        table.displayTable()
        table.isDealerTurn = True
        table.dealer.playTurn()
        table.displayTable()

        #Awarding hands
        table.evaluateRound()
        table.kickPlayer()

        #Quitting
        if len(table.players) == 0:
            print("looks like the house wins this time.")
            time.sleep(2)
            break

        print('would you like to keep playing? (YES/NO)')
        keepPlaying = input()
        while playing:
            if keepPlaying.upper() == 'YES':
                break
            elif keepPlaying.upper() == 'NO':
                playing = False
            else:
                keepPlaying = input('I didn"t understand that \n')

def exitPage():
    clearScreen()
    print("Thanks for playing, and Goodluck \n\n")
    print("Author: William Hickman")
    time.sleep(5)







nextPage = welcomePage()

if nextPage == 'PLAY':
    playGame()
elif nextPage == 'HELP':
    helpPage()
    playGame()

exitPage()

from doctest import FAIL_FAST
import numpy as np
import random
from player import Player
import time
from collections import namedtuple


Card = namedtuple('Card', 'value suit')


class Game():
    def __init__(self, nPlayers: int) -> None:
        self.deck = [ 
           Card('A','h'),
           Card('2','h'),
           Card('3','h'),
           Card('4','h'),
           Card('5','h'),
           Card('6','h'),
           Card('7','h'),
           Card('8','h'),
           Card('9','h'),
           Card('10','h'),
           Card('J','h'),
           Card('Q','h'),
           Card('K','h'),
           Card('A','d'),
           Card('2','d'),
           Card('3','d'),
           Card('4','d'),
           Card('5','d'),
           Card('6','d'),
           Card('7','d'),
           Card('8','d'),
           Card('9','d'),
           Card('10','d'),
           Card('J','d'),
           Card('Q','d'),
           Card('K','d'),
           Card('A','c'),
           Card('2','c'),
           Card('3','c'),
           Card('4','c'),
           Card('5','c'),
           Card('6','c'),
           Card('7','c'),
           Card('8','c'),
           Card('9','c'),
           Card('10','c'),
           Card('J','c'),
           Card('Q','c'),
           Card('K','c'),
           Card('A','s'),
           Card('2','s'),
           Card('3','s'),
           Card('4','s'),
           Card('5','s'),
           Card('6','s'),
           Card('7','s'),
           Card('8','s'),
           Card('9','s'),
           Card('10','s'),
           Card('J','s'),
           Card('Q','s'),
           Card('K','s')
        ]
        self.players = [Player(i+1) for i in range(nPlayers)]
        self.board = []
        self.nPlayers = nPlayers
        self.countHighCard = 0
        self.countPair = 0
        self.countTwoPair = 0
        self.countThreeOfAKind = 0
        self.countStraight = 0
        self.countFlush = 0
        self.countFullHouse = 0
        self.countFourOfAKind = 0
        self.countStraightFlush = 0
        self.countRoyalFlush = 0
        self.currentBet = 0.0
        self.pot = 0.0
        self.littleBlindValue = 1.0
        # always make the dealer the first player in the array
        self.dealer = self.players[0]
        self.userFold = False

        # generate the user player
        userIndex = random.randint(0, self.nPlayers - 1)
        self.players[userIndex].user = True

    def play(self, delay=False):
        """ Sequence of events for a complete game """
        self.shuffle()
        self.dealFirst()
        self.collectAnte()
        self.printInfo(1)
        self.betting()

        # first round of evaluation
        self.dealFlop()
        self.evaluatePlayers()
        if not self.userFold:
            self.printInfo(2)
            self.betting()
            if delay:
                time.sleep(3)

        # second round of evaluation
        self.dealSingleCard()
        self.evaluatePlayers()
        if not self.userFold:
            self.printInfo(3)
            self.betting()
            if delay:
                time.sleep(3)

        # third round of evaluation
        self.dealSingleCard()
        self.evaluatePlayers()
        if not self.userFold:
            self.printInfo(4)
            self.betting()

        self.determineWinner()
        
        # if delay:
            # time.sleep(3)
        # self.printFinalResults()
        # if gameNumber % 10000 == 0:
            # print(f"Game {gameNumber//1000}k")

    def printInfo(self, roundNumber):
        print("\n-----------------------")
        if roundNumber == 1:
            print(  "|                     |")
            print("-----------------------\n")
            user = None
            for player in self.players:
                if not player.user:
                    print(f"Player {player.number}:   --   - - ")
                else: user = player
            print(f"\nYou (${user.networth})\nPlayer {user.number}:   {user.hand:<15}   {user.card1.value}{user.card1.suit} {user.card2.value}{user.card2.suit}\n")
            return
        if roundNumber == 2:
            print(f"| {self.board[0].value}{self.board[0].suit}  {self.board[1].value}{self.board[1].suit}  {self.board[2].value}{self.board[2].suit}          |")
        if roundNumber == 3:
            print(f"| {self.board[0].value}{self.board[0].suit}  {self.board[1].value}{self.board[1].suit}  {self.board[2].value}{self.board[2].suit }  {self.board[3].value}{self.board[3].suit}      |")
        if roundNumber == 4:
            print(f"| {self.board[0].value}{self.board[0].suit}  {self.board[1].value}{self.board[1].suit}  {self.board[2].value}{self.board[2].suit }  {self.board[3].value}{self.board[3].suit}  {self.board[4].value}{self.board[4].suit} |")
        # for i in range(len(self.board)):
        #     print(f"| {self.board[i].value}{self.board[i].suit}", end='  ')
        print("-----------------------\n")
        user = None
        for player in self.players:
            if not player.user:
                # print(f"Player {player.number}:   {player.hand:<15}   {player.card1.value}{player.card1.suit} {player.card2.value}{player.card2.suit}")
                print(f"Player {player.number}:   --   - - ")
            else: user = player
        
        print(f"\nYou (${user.networth})\nPlayer {user.number}:   {user.hand:<15}   {user.card1.value}{user.card1.suit} {user.card2.value}{user.card2.suit}")

    def shuffle(self):
        """ Shuffles the deck randomly """
        random.shuffle(self.deck)



    def chooseCard(self) -> str:
        """ Removes the last card in the cards array and updates it """
        if len(self.deck) == 1:
            raise RuntimeError("There are no cards left!")
        return self.deck.pop()

    def dealFirst(self) -> None:
        """ Deals the first 2 cards to each player """
        for player in self.players:
            player.card1 = self.chooseCard()
            player.card2 = self.chooseCard()

    def dealSingleCard(self):
        self.board.append(self.chooseCard())

    def dealFlop(self, burner=False):
        if burner:
            self.deck.pop()
        for i in range(3):
            self.board.append(self.chooseCard())

    def performance(self):
        for player in self.players:
            print(f"Build Player Hand Array:")
            print('Has Hand Royal Flush:')
            player.hasHandRoyalFlush(self.board)
            print('Has Hand Straight Flush')
            player.hasHandStraightFlush(self.board)
            print('Has Hand Four of a Kind')
            player.hasHandFourOfAKind(self.board)
            print('Has Hand Full House')
            player.hasHandFullHouse(self.board)
            print('Has Hand Flush')
            player.hasHandFlush(self.board)
            print('Has Hand Straight')
            player.hasHandStraight(self.board)
            print('Has Hand Three of a Kind')
            player.hasHandThreeOfAKind(self.board)
            print('Has Hand Two Pair')
            player.hasHandTwoPair(self.board)
            print('Has Hand Pair')
            player.hasHandPair(self.board)

    def finalPlayerHands(self):
        """ Returns an array of the hand distribution for the game """
        return np.array([
            self.countHighCard,
            self.countPair,
            self.countTwoPair,
            self.countThreeOfAKind,
            self.countStraight,
            self.countFlush,
            self.countFullHouse,
            self.countFourOfAKind,
            self.countStraightFlush,
            self.countRoyalFlush,
        ],dtype=int)


    def evaluatePlayers(self):
        """ 
        Evaluate each player for their highest hand 
        Player method updates hand, tiebreaker member variable, returns bool
        Saves computation by not calculating any hands that are lowest than the highest
        """
        for player in self.players:
            if player.hasHandRoyalFlush(self.board):
                self.countRoyalFlush += 1
                continue
            elif player.hasHandStraightFlush(self.board):
                self.countStraightFlush += 1
                continue
            elif player.hasHandFourOfAKind(self.board):
                self.countFourOfAKind += 1
                continue
            elif player.hasHandFullHouse(self.board):
                self.countFullHouse += 1
                continue
            elif player.hasHandFlush(self.board):
                self.countFlush += 1
                continue
            elif player.hasHandStraight(self.board): 
                self.countStraight += 1
                continue
            elif player.hasHandThreeOfAKind(self.board):
                self.countThreeOfAKind += 1
                continue
            elif player.hasHandTwoPair(self.board):
                self.countTwoPair += 1
                continue
            elif player.hasHandPair(self.board):
                self.countPair += 1
                continue
            else:
                self.countHighCard += 1
                player.setHighCardTiebreaker(self.board)

    def comparePlayers(self, allPlayers):
        """
        Compares the tiebreaker array for all players considered
        Returns the player with the highest hand
        All players tiebreaker array will always have the same size
        """
        VALUE_DICT_ACE_HIGH = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        totalPlayers = len(allPlayers)
        nCards = len(allPlayers[0].tiebreaker)
        winner = allPlayers[0]
        tieArray = []
        tie = False
        for i in range(1, totalPlayers):
            for c in range(nCards):
                # if the cards are the same, move on to the next card in the tiebreaker array
                if VALUE_DICT_ACE_HIGH[winner.tiebreaker[c]] == VALUE_DICT_ACE_HIGH[allPlayers[i].tiebreaker[c]]:
                    # if the current card is the last and there is still no winner, tie
                    if c == nCards - 1:
                        tie = True
                        if winner not in tieArray:
                            tieArray.append(winner)    
                        tieArray.append(allPlayers[i]) 
                    continue
                # if the winner's card is worse, define the new winner
                tie = False
                if VALUE_DICT_ACE_HIGH[winner.tiebreaker[c]] < VALUE_DICT_ACE_HIGH[allPlayers[i].tiebreaker[c]]:
                    winner = allPlayers[i]
                    break
                # if the winner's card is better, don't look at any other cards
                break
        if tie:
            return tieArray
        return [winner]


    def determineWinner(self):
        """
        Compares each player's hands against each other. Returns array of player objects with highest player in first index
        """
        hand_rankings = {
            "high_card": 9,
            "pair": 8,
            "two_pair": 7,
            "three_of_a_kind": 6,
            "straight": 5,
            "flush": 4,
            "full_house": 3,
            "four_of_a_kind": 2,
            "straight_flush": 1,
            "royal_flush": 0
        }
        # create a 2D array of ranked player objects. Highest first index is winner
        # Second index is if there any any players with the same hand
        rankedHands = [ [],[],[],[],[],[],[],[],[],[] ]

        for player in self.players:
            index = hand_rankings[player.hand]
            # append to the array of the hand type for any additional players
            rankedHands[index].append(player)

        # iterate from best hand to worst. i: 0 -> 9
        # 0 is the best hand because it was defined this way in hand_rankings dict
        for i in range(10):
            currentPlayers = rankedHands[i]
            # if no current players have the specified hand, move on to the next
            if not currentPlayers:
                continue
            totalPlayers = len(currentPlayers)
            if not totalPlayers == 1:
                # else compare all players who have the same hand
                winner = self.comparePlayers(currentPlayers)
                # the compare player array has a distinct winner
                if len(winner) == 1:
                   print(f"\nWinner:     Player {winner[0].number}   {winner[0].hand}")
                   winner[0].printHand()
                   winner[0].networth += self.pot
                   return
                # the compare player array has multiple winners
                else:
                    print(f"\nTie Between Players:    {winner[0].hand}")
                    for i in range(len(winner)):
                        print(f"    Player {winner[i].number}:") 
                        winner[i].printHand()
                        winner[i].networth += (self.pot / len(winner))
                    return 
            # if there is only one player, they automatically win
            print(f"\nWinner:     Player {currentPlayers[0].number}   {currentPlayers[0].hand}")
            currentPlayers[0].printHand()
            currentPlayers[0].networth += self.pot
            return

    def betting(self):
        for player in self.players[1:]:
            if player.user:
                print(f"The current bet is ${self.bet}. Would you like to check, call, raise, or fold?")
                betMade = False 
                while True:
                    if betMade:
                        break
                    decision = input("x / c / r / f :     ")
                    if decision == "x":
                        break
                    elif decision == "c":
                        player.networth -= self.bet
                        self.pot += self.bet
                        break
                    elif decision == "r":
                        while True:
                            raiseAmount = float(input("Amount: "))
                            if raiseAmount > player.networth:
                                print("Bet too large!")
                            else:
                                player.networth -= float(raiseAmount)
                                self.bet += float(raiseAmount)
                                self.pot += self.bet
                                betMade = True
                                break
                    elif decision == "f":
                        self.userFold = True
                        break
                    else:
                        print("Please enter a valid option.")
                    
            else:
                # AI betting
                pass
                # just call the current bet
                player.networth -= self.bet
                self.pot += self.bet
        

    def collectAnte(self):
        bigBlind = self.littleBlindValue * 2
        self.bet = bigBlind
        try:
            self.dealer.networth -= self.littleBlindValue
        except:
            self.dealer.networth < self.littleBlindValue
        for player in self.players:
            try:
                player.networth -= (bigBlind * 2)
            except:
                player.networth < (bigBlind * 2)
    
    

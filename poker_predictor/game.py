from dataclasses import dataclass
from threading import local
import numpy as np
import random
# from player import Player
# from non_numpy_player import Player
from hybrid_player import Player
import time

@dataclass
class Card:
    value: str
    suit: str

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

# always want to rank ace as the highest, only consider it being lowest in ex. determine straight method
value_rankings = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    '10': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

class Game:
    def __init__(self, nPlayers: int) -> None:
        self.players = [Player() for i in range(nPlayers)]
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
        self.board = []
        self.nPlayers = nPlayers

    def play(self, gameNumber, delay=False):
        """ Sequence of events for a complete game """
        self.shuffle()
        self.dealFirst()

        # first round of evaluation
        # self.evaluatePlayers()
        # self.printInfo(1)
        if delay:
            time.sleep(3)

        # second round of evaluation
        self.dealFlop()
        # self.evaluatePlayers()
        # self.printInfo(2)
        if delay:
            time.sleep(3)

        # third round of evaluation
        self.dealSingleCard()
        # self.evaluatePlayers()
        # self.printInfo(3)
        if delay:
            time.sleep(3)

        # final round of evaluation
        self.dealSingleCard()
        # self.performance()
        self.evaluatePlayers()
        # self.printInfo(4)
        if delay:
            time.sleep(3)
        # self.printFinalResults()
        if gameNumber % 10000 == 0:
            print(f"Game {gameNumber//1000}k")

    def printInfo(self, roundNumber):
        print("\n-----------------------")
        if roundNumber == 1:
            print(  "|                     |")
        if roundNumber == 2:
            print(f"| {self.board[0].value}{self.board[0].suit}  {self.board[1].value}{self.board[1].suit}  {self.board[2].value}{self.board[2].suit}          |")
        if roundNumber == 3:
            print(f"| {self.board[0].value}{self.board[0].suit}  {self.board[1].value}{self.board[1].suit}  {self.board[2].value}{self.board[2].suit }  {self.board[3].value}{self.board[3].suit}      |")
        if roundNumber == 4:
            print(f"| {self.board[0].value}{self.board[0].suit}  {self.board[1].value}{self.board[1].suit}  {self.board[2].value}{self.board[2].suit }  {self.board[3].value}{self.board[3].suit}  {self.board[4].value}{self.board[4].suit} |")
        # for i in range(len(self.board)):
        #     print(f"| {self.board[i].value}{self.board[i].suit}", end='  ')
        print("-----------------------\n")
        for i,ele in enumerate(self.players):
            print(f"Player {i+1}:   {ele.hand:<15}   {ele.card1.value}{ele.card1.suit} {ele.card2.value}{ele.card2.suit}")

    def shuffle(self):
        """ Shuffles the deck randomly """
        random.shuffle(self.deck)



    # TODO(Catch error if too many players and run out of cards)
    def chooseCard(self) -> str:
        """ Removes the last card in the cards array and updates it """
        return self.deck.pop()

    def dealFirst(self) -> None:
        """ Deals the first 2 cards to each player """
        for player in self.players:
            player.card1 = self.chooseCard()
            player.card2 = self.chooseCard()

    def dealSingleCard(self):
        self.board.append(self.chooseCard())

    def dealFlop(self):
        #TODO(Add a burner card function)
        for i in range(3):
            self.board.append(self.chooseCard())

    def performance(self):
        for player in self.players:
            print(f"Build Player Hand Array:")
            # player.buildPlayerHandArray(self.board)
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

    def evaluatePlayers(self):
        """ 
        Evaluate each player for their highest hand 
        Player method updates hand member variable, returns bool
        Saves computation by not calculating any hands that are lowest than the highest
        """
        for player in self.players:
            # build the player's card array
            # player.buildPlayerHandArray(self.board)
            if player.hasHandRoyalFlush(self.board):
                # if len(self.board) == 5:
                    # print('Royal flush')   
                # print('Royal flush!!\n')
                # print(f"{player.card1.value}{player.card1.suit} {player.card2.value}{player.card2.suit}\n {self.board}\n")
                continue
            elif player.hasHandStraightFlush(self.board): continue
            elif player.hasHandFourOfAKind(self.board): continue
            elif player.hasHandFullHouse(self.board): continue
            elif player.hasHandFlush(self.board): continue
            elif player.hasHandStraight(self.board): continue
            elif player.hasHandThreeOfAKind(self.board): continue
            elif player.hasHandTwoPair(self.board): continue
            elif player.hasHandPair(self.board): continue
            # probably not needed because each player is initalized with high_card
            # else: player.setHighCardHand()

    

    # TODO(Test the fuck out of this)
    def compareHighCardTwoPlayers(self, allPlayers):
        """ Compares high card array to another player. Returns winner player object """
        # for i in range(7):
        #     selfCard = value_rankings[self.high_card[i]]
        #     otherCard = value_rankings[other.high_card[i]]
        #     # keep going until the cards are different
        #     if selfCard == otherCard:
        #         continue
        #     if selfCard < otherCard:
        #         return other
        #     else:
        #         return self

    def compareHighCard(self, allPlayers):
        """
        Compares players with a high card. Returns winner player object
        """
        pass

    def comparePair(self, allPlayers):
        """
        Compares players with a pair. Returns winner player object

        """
        # first compare the value of the hand

        # if the value is the same, move on to high card check
        

    def compareTwoPair(self, allPlayers):
        """
        Compares players with a pair. Returns winner player object

        RULES:
        1) Highest pair
        2) 1 kicker card
        """
        # first compare the value of the hand

        # if the value is the same, move on to high card check


    def compareThreeOfAKind(self, allPlayers):
        """
        Compares players with a three of a kind. Returns winner player object

        RULES:
        1) Highest three of a kind wins, doesn't matter the suit
        2) First kicker card
        3) Second kicker card
        """
        # first compare the value of the hand

        # if the value is the same, move on to high card check

    def compareFullHouse(self, allPlayers):
        """
        Compares players with a full house. Returns winner player object 
        
        RULES:
        1) Higher three of a kind
        2) Higher pair
        3) Exact same hand, split the pot 
        
        """
        pass

    def compareFlush(self, allPlayers):
        """
        Compares players with a flush. Returns winner player object

        RULES:
        1) Highest flush wins, doesn't matter the suit
        2) If same high card, move on to the next, etc.
        3) If all 5 cards are exactly the same value, split the pot
        """
        pass

    def compareStraight(self, allPlayers):
        """
        Compares players with a straight. Returns winner player object

        RULES:
        Highest straight wins, doesn't matter the suit

        """
        pass

    def compareFourOfAKind(self, allPlayers):
        """
        Compares players with a four a kind. Returns winner player object

        """
        # first compare the value of the hand

        # if the value is the same, move on to high card check

    #NOTE Probably never will get a scenario where two players both have straight flushes
    def compareStraightFlush(self, other):
        """
        Compares players with a four a kind. Returns winner player object

        """
        # first compare the value of the hand

        # if the value is the same, move on to high card check

    #NOTE impossible to get two royal flushes in Texas Hold Em'

    def determineRoundWinner(self):
        """
        Compares each player's hands against each other. Returns array of player objects with highest player in first index
        """
        # create a 2D array of ranked player objects. Highest first index is winner
        # Second index is if there any any players with the same hand
        rankedHands = np.empty((self.nPlayers, self.nPlayers))
        for player in self.players:
            index = hand_rankings[player.hand]
            # append to the array of the hand type for any additional players
            rankedHands[index] = np.append(rankedHands[index], player)

        # iterate from best hand to worst. i: 0 -> 9
        # 0 is the best hand because it was defined this way in hand_rankings dict
        for i in range(10):
            currentPlayers = rankedHands[i]
            # if no current players have the specified hand, move on to the next
            if currentPlayers:
                totalPlayers = len(currentPlayers)
                # if there is only one player, they automatically win
                if totalPlayers == 1:
                    return currentPlayers[0]
                # else compare all players who have the same hand
                return self.compareHands(i, currentPlayers)


    def compareHands(self, rankIndex, currentPlayers):
        """
        Compares players hands for each specified hand type. Returns winner player object
        """
        if rankIndex == 9:
            return self.compareHighCard(currentPlayers)
        elif rankIndex == 8:
            return self.comparePair(currentPlayers)
        elif rankIndex == 7:
            return self.compareTwoPair(currentPlayers)
        elif rankIndex == 6:
            return self.compareThreeOfAKind(currentPlayers)
        elif rankIndex == 5:
            return self.compareFlush(currentPlayers)
        elif rankIndex == 4:
            return self.compareStraight(currentPlayers)
        elif rankIndex == 3:
            return self.compareFullHouse(currentPlayers)
        elif rankIndex == 2:
            return self.compareFourOfAKind(currentPlayers)
        elif rankIndex == 1:
            return self.compareStraightFlush(currentPlayers)
        elif rankIndex == 0:
            pass
            # not possible for two players to have a royal flush
    

    def printFinalResults(self):
        pass

    

    

    












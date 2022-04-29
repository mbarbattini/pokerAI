from dataclasses import dataclass
import numpy as np
import random

# player struct
@dataclass
class Player():
    card1: str = None
    card2: str = None
    hand = "high_card"
    probability: float = None

# board struct
@dataclass
class Board():
    cards: str = []

# deck struct
@dataclass
class Deck():
    cards = [
        "ac","2c","3c","4c","5c","6c","7c","8c","9c","10c","jc","qc","kc",
        "as","2s","3s","4s","5s","6s","7s","8s","9s","10s","js","qs","ks",
        "ad","2d","3d","4d","5d","6d","7d","8d","9d","10d","jd","qd","kd",
        "ah","2h","3h","4h","5h","6h","7h","8h","9h","10h","jh","qh","kh",
    ]

    # could use mod math to get the suit. value % 4 = 0 -> heart
    #                                               = 1 -> club
    #                                               = 2 -> spade
    #                                               = 3 -> diamond
    cards_dict = {
        "ac": 1,
        "as": 2,
        "ad": 3,
        "ah": 4,
        "2c": 5, 
        "2s": 6, 
        "2d": 7,
        "2h": 8,
        "3c": 9,
        "3s": 10,
        "3d": 11,
        "3h": 12,
        "4c": 13,
        "4s": 14,
        "4d": 15,
        "4h": 16,
        "5c": 17,
        "5s": 18,
        "5d": 19,
        "5h": 20,
        "6c": 21,
        "6s": 22,
        "6d": 23,
        "6h": 24,
        "7c": 25,
        "7s": 26,
        "7d": 27,
        "7h": 28,
        "8c": 29,
        "8s": 30,
        "8d": 31,
        "8h": 32,
        "9c": 33,
        "9s": 34,
        "9d": 35,
        "9h": 36,
        "10c": 37,
        "10s": 38,
        "10d": 39,
        "10h": 40,
        "jc": 41,
        "js": 42,
        "jd": 43,
        "jh": 44,
        "qc": 45,
        "qs": 46,
        "qd": 47,
        "qh": 48,
        "kc": 49,
        "ks": 50,
        "kd": 51,
        "kh": 52
    }

class Game():
    def __init__(self, nPlayers: int) -> None:
        self.players = [Player() for i in range(nPlayers)]
        self.deck = Deck()
        self.board = Board()

    def play(self):
        """ Sequence of events for a complete game """
        self.shuffle()
        self.dealFirst()
        # first round of evaluation
        # self.evaluatePlayers()
        self.printInfo()
        # second round of evaluation
        self.dealFlop()
        self.evaluatePlayers()
        self.printInfo()
        # third round of evaluation
        self.dealSingleCard()
        self.evaluatePlayers()
        self.printInfo()
        # final round of evaluation
        self.dealSingleCard()
        self.evaluatePlayers()
        self.printInfo()
        self.printFinalResults()

    def printInfo(self) -> None:
        for i,ele in enumerate(self.players):
            print(f"Player {i+1}:   {ele.hand} ({ele.card1} {ele.card2})    {ele.probability}%")

    def shuffle(self):
        """ Shuffles the deck randomly """
        random.shuffle(self.deck.cards)

    # TODO(Should it be the highest hand or all possible hands?)
    # TODO(Determining a straight as a set of many numbers and choosing a subset that is in ascending order. Leetcode problem)
    def playerHand(self) -> str:
        """ Returns a boolean array of all possible hands the player currently has """

        self.players[0].hand()

        number1 = self.card1[0]
        suit1 = self.card1[1]
        number2 = self.card2[0]
        suit2 = self.card2[1]

        if number1 == number2:
            return "pair"
        elif suit1 == suit2:
            return "suited"
        else:
            return

    # TODO(Catch error if too many players and run out of cards)
    def choose(self) -> str:
        """ Removes the last card in the cards array and updates it """
        return self.deck.cards.pop()

    def dealFirst(self) -> None:
        """ Deals the first 2 cards to each player """
        for player in self.players:
            player.card1 = self.choose()
            player.card2 = self.choose()

    def dealSingleCard(self):
        pass

    def dealFlop(self):
        #TODO(Add a burner card function)
        for i in range(3):
            self.board.append(self.deck.cards.pop())

    def evaluatePlayers(self):
        pass

    def printFinalResults(self):
        pass




def main():

    numberPlayers = 5

    game = Game(numberPlayers)

    game.play()




if __name__== "__main__":
    main()





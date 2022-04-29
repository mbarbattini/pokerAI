from dataclasses import dataclass
import numpy as np
import random

# player struct
@dataclass
class Player():
    card1 = None
    card2 = None
    hand = "high_card"
    probability = None

# could use mod math to get the suit. value % 4 = 0 -> heart
#                                               = 1 -> club
#                                               = 2 -> spade
#                                               = 3 -> diamond
cards_dict = {
    "Ac": 1,
    "As": 2,
    "Ad": 3,
    "Ah": 4,
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
    "Jc": 41,
    "Js": 42,
    "Jd": 43,
    "Jh": 44,
    "Qc": 45,
    "Qs": 46,
    "Qd": 47,
    "Qh": 48,
    "Kc": 49,
    "Ks": 50,
    "Kd": 51,
    "Kh": 52
}

class Game():
    def __init__(self, nPlayers: int) -> None:
        self.players = [Player() for i in range(nPlayers)]
        self.deck = [
            "Ac","2c","3c","4c","5c","6c","7c","8c","9c","10c","Jc","Qc","Kc",
            "As","2s","3s","4s","5s","6s","7s","8s","9s","10s","Js","Qs","Ks",
            "Ad","2d","3d","4d","5d","6d","7d","8d","9d","10d","Jd","Qd","Kd",
            "Ah","2h","3h","4h","5h","6h","7h","8h","9h","10h","Jh","Qh","Kh",
        ]
        self.board = []

    def play(self):
        """ Sequence of events for a complete game """
        self.shuffle()
        self.dealFirst()
        # first round of evaluation
        # self.evaluatePlayers()
        self.printInfo()
        # second round of evaluation
        self.dealFlop()

        self.numberFrequency(self.players[0])

        # self.evaluatePlayers()
        # self.printInfo()
        # # third round of evaluation
        # self.dealSingleCard()
        # self.evaluatePlayers()
        # self.printInfo()
        # # final round of evaluation
        # self.dealSingleCard()
        # self.evaluatePlayers()
        # self.printInfo()
        # self.printFinalResults()

    def printInfo(self) -> None:
        for i,ele in enumerate(self.players):
            print(f"Player {i+1}:   {ele.hand} ({ele.card1} {ele.card2})    {ele.probability}%")

    def shuffle(self):
        """ Shuffles the deck randomly """
        random.shuffle(self.deck)

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

    def evaluatePlayers(self):
        pass

    def printFinalResults(self):
        pass

    def numberFrequency(self, player):
        """ Returns an array of all cards and the number of each currently held by the player """
        frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # cards currently held by the player
        number1 = player.card1[:-1]
        number2 = player.card2[:-1]

        value_dict = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}

        frequency[value_dict[number1]] += 1
        frequency[value_dict[number2]] += 1

         # add on the cards from the board
        for card in self.board:
            frequency[value_dict[card[:-1]]] += 1

        return frequency

    def suitFrequency(self, player):
        """ Returns an array of all suits and the number of each currently held by the player """
        # [club, spades, diamond, heart]
        frequency = [0, 0, 0, 0]

        suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}

        # cards currently held by the player
        suit1 = player.card1[-1]
        suit2 = player.card2[-1]

        frequency[suit_dict[suit1]] += 1
        frequency[suit_dict[suit2]] += 1

        # add on the cards from the board
        for card in self.board:
            frequency[suit_dict[card[-1]]] += 1

        return frequency




def main():

    numberPlayers = 5

    game = Game(numberPlayers)

    game.play()




if __name__== "__main__":
    main()





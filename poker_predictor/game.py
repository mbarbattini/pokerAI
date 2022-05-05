import numpy as np
import random
from .player import Player


class Game:
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
            print(f"Player {i+1}:   {ele.hand} ({ele.card1} {ele.card2})    {ele.probability*100}%")

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

    def evaluatePlayers(self):
        """ evaluate the player for all possible hands """
        for player in self.players:
            if player.hasHandRoyalFlush(self.board):
                break
            elif player.hasHandStraightFlush(self.board):
                break
            elif player.hasHandFourOfAKind(self.board):
                break
            elif player.hasHandFullHouse(self.board):
                break
            elif player.hasHandFlush(self.board):
                break
            elif player.hasHandStraight(self.board):
                break
            elif player.hasHandThreeOfAKind(self.board):
                break
            elif player.hasHandTwoPair(self.board):
                break
            elif player.hasHandPair(self.board):
                break
            else:
                player.setHighCardHand()

    def printFinalResults(self):
        pass

    

    

    












from .board import Board
from .deck import Deck

class Player:
    def __init__(self) -> None:
        self.card1 = None
        self.card2 = None

    # TODO(Should it be the highest hand or all possible hands?)
    def hand(self) -> str:
        """ Returns the string of the highest hand the player holds """
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
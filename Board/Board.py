from Deck import *

class Board:
    def __init__(self) -> None:
        self.cards = []

    def addCard(self):
        if self.cards >= 4:
            return "Error."
        else:

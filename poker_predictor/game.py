from .player import Player
from .deck import Deck

class Game:
    def __init__(self, nPlayers: int) -> None:
        self.players = [Player() for i in range(nPlayers)]
        self.deck = Deck()
        self.board = None
    
    def start(self) -> None:
        pass

    def printInfo(self) -> None:
        for i,ele in enumerate(self.players):
            print(f"Player {i}: {ele.hand()} ({ele.card1} {ele.card2})")

    def dealPlayer(self):
        

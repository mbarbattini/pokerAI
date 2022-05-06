# from poker_predictor import Player, Game
from player import Player
from game import Game

def main():

    numberPlayers = 8
    delay = 3
    numberGames = 10000

    for i in range(numberGames):

        game = Game(numberPlayers)
        game.play(delay)




if __name__== "__main__":
    main()
# from poker_predictor import Player, Game
from player import Player
from game import Game
import time

def main():

    numberPlayers = 1
    delay = 3
    numberGames = 2000000

    start = time.time()
    for i in range(numberGames):

        game = Game(numberPlayers)
        game.play(delay)
    
    print(f"\nComputation time: {(time.time()-start) /60} min\n")




if __name__== "__main__":
    main()
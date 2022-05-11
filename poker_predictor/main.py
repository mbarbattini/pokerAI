# from poker_predictor import Player, Game
from player import Player
from game import Game
import time
import numpy as np

def main():

    numberPlayers = 1
    numberGames = 2000000

    handFrequency = np.zeros((10),dtype=int)
    start = time.time()
    for i in range(numberGames):
        game = Game(numberPlayers)
        game.play()
        handFrequency += game.finalPlayerHands()


    print(f"\nComputation time: {(time.time()-start) /60} min\n")

    for ele in reversed(handFrequency):
        print(ele)




if __name__== "__main__":
    main()
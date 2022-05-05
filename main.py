from poker_predictor import Player, Game

def main():

    # numberPlayers = 5

    # game = Game(numberPlayers)

    # game.play()

    player1 = Player()
    player2 = Player()

    player1.card1 = '3d'
    player1.card2 = '4s'

    player2.card1 = '7s'
    player2.card2 = '8d'

    board = ['3s','4h','4d','10h','Kh']

    print(player2.hasHandFullHouse(board))
    # print(player1.hasHandTwoPair(board))
    # print(player2.hasHandPair(board))
    # print(player2.hasHandTwoPair(board))







if __name__== "__main__":
    main()
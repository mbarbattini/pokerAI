from poker_predictor import Game

def main():

    number_players = 5

    game = Game(number_players)

    # shuffle the deck to start
    game.shuffle()
    # deal cards to all players
    game.deal()
    




if __name__== '__main__':
    main()
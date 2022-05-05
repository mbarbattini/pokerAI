import numpy as np
import random

# # could use mod math to get the suit. value % 4 = 0 -> heart
# #                                               = 1 -> club
# #                                               = 2 -> spade
# #                                               = 3 -> diamond
# cards_dict = {
#     "Ac": 1,
#     "As": 2,
#     "Ad": 3,
#     "Ah": 4,
#     "2c": 5, 
#     "2s": 6, 
#     "2d": 7,
#     "2h": 8,
#     "3c": 9,
#     "3s": 10,
#     "3d": 11,
#     "3h": 12,
#     "4c": 13,
#     "4s": 14,
#     "4d": 15,
#     "4h": 16,
#     "5c": 17,
#     "5s": 18,
#     "5d": 19,
#     "5h": 20,
#     "6c": 21,
#     "6s": 22,
#     "6d": 23,
#     "6h": 24,
#     "7c": 25,
#     "7s": 26,
#     "7d": 27,
#     "7h": 28,
#     "8c": 29,
#     "8s": 30,
#     "8d": 31,
#     "8h": 32,
#     "9c": 33,
#     "9s": 34,
#     "9d": 35,
#     "9h": 36,
#     "10c": 37,
#     "10s": 38,
#     "10d": 39,
#     "10h": 40,
#     "Jc": 41,
#     "Js": 42,
#     "Jd": 43,
#     "Jh": 44,
#     "Qc": 45,
#     "Qs": 46,
#     "Qd": 47,
#     "Qh": 48,
#     "Kc": 49,
#     "Ks": 50,
#     "Kd": 51,
#     "Kh": 52
# }


# always want to rank ace as the highest, only consider it being lowest in ex. determine straight method
value_rankings = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    '10': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

hand_rankings = {
    "high_card": 1,
    "pair": 2,
    "two_pair": 3,
    "three_of_a_kind": 4,
    "straight": 5,
    "flush": 6,
    "full_house": 7,
    "four_of_a_kind": 8,
    "straight_flush": 9,
    "royal_flush": 10
}

class Player():
    def __init__(self):
        self.card1 = None
        self.card2 = None
        self.hand = "high_card"
        # can have 1 element (pair) 2 elements (full house)
        self.handValue = []
        self.probability = None
        # an array with 7 elements, worst case is two players have exact same high card up until the last one
        # Player 1: [10,9,8,7,6,5,4]
        # Player 2: [10,9,8,7,6,5,2]
        self.high_card = []

    def numberFrequency(self, board):
        """ Returns an array of all cards and the number of each currently held by the player """
        frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # cards currently held by the player
        number1 = self.card1[:-1]
        number2 = self.card2[:-1]

        value_dict = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}

        frequency[value_dict[number1]] += 1
        frequency[value_dict[number2]] += 1

         # add on the cards from the board
        for card in board:
            frequency[value_dict[card[:-1]]] += 1

        return frequency

    def suitFrequency(self, board):
        """ Returns an array of all suits and the number of each currently held by the player """
        # [club, spades, diamond, heart]
        frequency = [0, 0, 0, 0]

        suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}

        # cards currently held by the player
        suit1 = self.card1[-1]
        suit2 = self.card2[-1]

        frequency[suit_dict[suit1]] += 1
        frequency[suit_dict[suit2]] += 1

        # add on the cards from the board
        for card in board:
            frequency[suit_dict[card[-1]]] += 1

        return frequency

    def handRank(self):
        return hand_rankings[self.hand]

    # TODO(Should it be the highest hand or all possible hands?) Probably just the highest
    # def hands(self):
    #     """ Returns a boolean array of all possible hands the player currently has """

    #     number1 = self.card1[0]
    #     number2 = self.card2[0]
    #     suit1 = self.card1[1]
    #     suit2 = self.card2[1]

    #     # if number1 == number2:
    #     #     return "pair"
    #     # elif suit1 == suit2:
    #     #     return "suited"
    #     # else:
    #     #     return

    def setHighCard(self):
        """ Assigns the high_card variable in order from best to worst """
        pass

    # TODO(Test the fuck out of this)
    def compareHighCard(self, other):
        """ Compares high card to another player. Returns winner player object """
        for i in range(7):
            selfCard = value_rankings[self.high_card[i]]
            otherCard = value_rankings[other.high_card[i]]
            # keep going until the cards are different
            if selfCard == otherCard:
                continue
            if selfCard < otherCard:
                return other
            else:
                return self

    def compareFullHouse(self, other):
        """
        Compares two players with a full house. Returns winner player object 
        
        RULES:
        1) Higher three of a kind
        2) Higher pair
        3) Exact same hand, split the pot 
        
        """
        pass

    def compareFlush(self, other):
        """
        Compares two players with a flush. Returns winner player object

        RULES:
        Highest flush wins, doesn't matter the suit

        """

    def assignHighCardHand(self):
        self.hand = 'high_card'

    def hasHandPair(self, board):
        valid = False

        if valid: self.hand = 'pair'
        return valid

    def hasHandTwoPair(self, board):
        valid = False

        if valid: self.hand = 'two_pair'
        return valid

    def hasHandThreeOfAKind(self, board):
        valid = False

        if valid: self.hand = 'three_of_a_kind'
        return valid

    def hasHandFlush(self, board):
        valid = False

        if valid: self.hand = 'flush'
        return valid

    # TODO(Determining a straight as a set of many numbers and choosing a subset that is in ascending order. Leetcode problem)
    def hasHandStraight(self, board):
        #NOTE straights cannot wrap around
        valid = False

        if valid: self.hand = 'straight'
        return valid

    def hasHandFullHouse(self, board):
        valid = False

        if valid: self.hand = 'full_house'
        return valid

    def hasHandFourOfAKind(self, board):
        valid = False

        if valid: self.hand = 'four_of_a_kind'
        return valid

    def hasHandStraightFlush(self, board):
        valid = False

        if valid: self.hand = 'striaght_flush'
        return valid

    def hasHandRoyalFlush(self, board):
        valid = False

        if valid: self.hand = 'royal_flush'
        return valid

    def evaluateFullHouse(self, board):
        """ Determines the chances of the player getting a full house on the next sequence """
        outcome = 0
        # dont evaluate if player's current hand is better than a full house
        if self.handRank() < hand_rankings["full house"]:
            for ele in self.numberFrequency():
                if ele == 2:
                    # when 
                    pass
                if ele == 3:
                    #
                    pass

        return outcome



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
            print(f"Player {i+1}:   {ele.hands} ({ele.card1} {ele.card2})    {ele.probability}%")

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
                player.assignHighCardHand()

    def printFinalResults(self):
        pass

    

    

    






def main():

    numberPlayers = 5

    game = Game(numberPlayers)

    game.play()




if __name__== "__main__":
    main()





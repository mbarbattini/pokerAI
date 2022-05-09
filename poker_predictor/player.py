# always want to rank ace as the highest, only consider it being lowest in ex. determine straight method
import numpy as np
from dataclasses import dataclass

@dataclass
class Card:
    value: str
    suit: str

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

class Player:
    
    def __init__(self):
        self.card1 = None
        self.card2 = None
        self.hand = "high_card"
        self.probability = None
        # an array with 7 elements, worst case is two players have exact same high card up until the last one
        # Player 1: [10,9,8,7,6,5,4]
        # Player 2: [10,9,8,7,6,5,2]
        self.high_card = []
        self.cardArray = None

    def buildPlayerHandArray(self, board, aceHigh=False):
        """
        Creates a 2D array of shape (13, 4) of all possible cards ranked from worst to best (lowest index -> highest index)
        """
        suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}
        value_dict = None
        if aceHigh:
            value_dict = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        else:
            value_dict = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}

        localBoard = np.append(board, [self.card1,self.card2])

        cardsArr = np.empty((13,4), dtype=Card)
        for card in localBoard:
            indexValue = value_dict[card.value]
            indexSuit = suit_dict[card.suit]
            cardsArr[indexValue,indexSuit] = card

        self.cardArray = cardsArr

    # def numberFrequency(self, board):
    #     """ Returns an array of all cards and the number of each currently held by the player """
    #     frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    #     # cards currently held by the player
    #     number1 = self.card1.value
    #     number2 = self.card2.value

    #     value_dict = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}

    #     frequency[value_dict[number1]] += 1
    #     frequency[value_dict[number2]] += 1

    #      # add on the cards from the board
    #     for card in board:
    #         frequency[value_dict[card.value]] += 1

    #     return frequency

    # def suitFrequency(self, board):
    #     """ Returns an array of all suits and the number of each currently held by the player """
    #     # [club, spades, diamond, heart]
    #     frequency = [0, 0, 0, 0]

    #     suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}

    #     # cards currently held by the player
    #     suit1 = self.card1.suit
    #     suit2 = self.card2.suit

    #     frequency[suit_dict[suit1]] += 1
    #     frequency[suit_dict[suit2]] += 1

    #     # add on the cards from the board
    #     for card in board:
    #         frequency[suit_dict[card.suit]] += 1

    #     return frequency

    def setHighCard(self):
        """ Assigns the high_card array in order from best to worst """
        pass
    
    def setHighCardHand(self):
        self.hand = 'high_card'

    def hasHandPair(self, board):
        """ Determines if the player has a pair """
        self.buildPlayerHandArray(board)
        for i in range(13):
            valueArray = self.cardArray[i,:]
            if np.count_nonzero(valueArray) >= 2:
                self.hand = 'pair'
                return True
        return False

    def hasHandTwoPair(self, board):
        """ Determines if the player has a two pair """
        self.buildPlayerHandArray(board)
        count = 0
        for i in range(13):
            valueArray = self.cardArray[i,:]
            if np.count_nonzero(valueArray) == 2:
                count += 1
                if count >= 2:
                    self.hand = 'two_pair'
                    return True
        return False

    def hasHandThreeOfAKind(self, board):
        """  Determines if the player has a three of a kind """
        self.buildPlayerHandArray(board)
        for i in range(13):
            count = 0
            valueArray = self.cardArray[i,:]
            if np.count_nonzero(valueArray) >= 3:
                self.hand = 'three_of_a_kind'
                return True
        return False

    def hasHandFlush(self, board):
        """ Determines if the player has a flush """
        self.buildPlayerHandArray(board)

        for i in range(4):
            suitArray = self.cardArray[:,i]
            if np.count_nonzero(suitArray) >= 5:
                self.hand = 'flush'
                return True
        return False

    def hasHandStraight(self, board):
        """ Determines if the player has a straight """

        self.buildPlayerHandArray(board)

        for i in range(13):
            count = 0
            valueArray = self.cardArray[i,:]
            if np.count_nonzero(valueArray) >= 1:
                count += 1
                if count >= 5:
                    self.hand = 'straight'
                    return True
            else:
                count = 0
        return False

    def hasHandFullHouse(self, board):
        """ Determines if the player has a full house """
        self.buildPlayerHandArray(board)
        valid = False
        for i in range(13):
            valueArray = self.cardArray[i,:]
            if np.count_nonzero(valueArray) == 3:
                # loop through the rest
                for j in range(i,13):
                    if np.count_nonzero(self.cardArray[j,:]) == 2:
                        valid = True
            elif np.count_nonzero(valueArray) == 2:
                for j in range(i,13):
                    if np.count_nonzero(self.cardArray[j,:]) == 3:
                        valid = True
            elif valid:
                self.hand = 'full_house'
                return True
            else:
                count = 0
        return False

    def hasHandFourOfAKind(self, board):
        """ Determines if the player has a four of a kind
        Boolean return, does not determine the value of the four of a kind """
        self.buildPlayerHandArray(board)

        for i in range(13):
            valueArray = self.cardArray[i,:]
            if np.count_nonzero(valueArray) == 4:
                self.hand = 'four_of_a_kind'
                return True
        return False
            
    def hasHandStraightFlush(self, board):
        """" Check if the player has a straight flush """
        self.buildPlayerHandArray(board)

        # iterate through each suit array and try to find successive entries
        for i in range(4):
            count = 0
            # get all cards of a single suit
            suitArray = self.cardArray[:,i]
            for card in suitArray:
                # if there is a card, add to count
                if card:
                    count += 1
                    # as soon as count is 5, successful
                    if count >= 5:
                        self.hand = 'straight_flush'
                        return True
                else:
                    count = 0
            
        return False

    def hasHandRoyalFlush(self, board):
        """ Determines if the player has a royal flush """
        self.buildPlayerHandArray(board, aceHigh=True)
        for i in range(4):
            count = 0
            # get all royal cards of a single suit
            suitArray = self.cardArray[-5:,i]
            for card in suitArray:
                # if there is a card, add to count
                if card:
                    count += 1
                    if count >= 5:
                        self.hand = 'royal_flush'
                        return True
                else:
                    count = 0
        return False


    # def bubbleSort(self, arr):
    #     suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}
    #     value_dict = {'A': 13, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}
    #     # [lowest ... highest]
    #     n = len(arr)

    #     for i in range(n):
    #         for j in range(0, n-i-1):
    #             if value_dict[arr[j].value] > value_dict[arr[j+1].value]:
    #                 # swap
    #                 arr[j], arr[j+1] = arr[j+1], arr[j]

    #     return arr

    def evaluateFullHouse(self, board):
        """ Determines the chances of the player getting a full house on the next sequence """
        outcome = 0
        for ele in self.numberFrequency():
            if ele == 2:
                # when 
                pass
            if ele == 3:
                #
                pass

        return outcome
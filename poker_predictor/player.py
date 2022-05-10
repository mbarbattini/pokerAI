import sys
from time import perf_counter
from functools import wraps


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = f(*args, **kwargs)
        end = perf_counter()
        print(f'{(end-start)*1e6} us\n')
        return result
    return wrapper

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

    def numberFrequency(self, board):
        """ Returns an array of all cards and the number of each currently held by the player """
        frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # cards currently held by the player
        number1 = self.card1.value
        number2 = self.card2.value

        value_dict = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}

        frequency[value_dict[number1]] += 1
        frequency[value_dict[number2]] += 1

         # add on the cards from the board
        for card in board:
            frequency[value_dict[card.value]] += 1

        return frequency

    def suitFrequency(self, board):
        """ Returns an array of all suits and the number of each currently held by the player """
        # [club, spades, diamond, heart]
        frequency = [0, 0, 0, 0]

        suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}

        # cards currently held by the player
        suit1 = self.card1.suit
        suit2 = self.card2.suit

        frequency[suit_dict[suit1]] += 1
        frequency[suit_dict[suit2]] += 1

        # add on the cards from the board
        for card in board:
            frequency[suit_dict[card.suit]] += 1

        return frequency

    def setHighCard(self):
        """ Assigns the high_card array in order from best to worst """
        pass
    
    def setHighCardHand(self):
        self.hand = 'high_card'

    # @timing
    def hasHandPair(self, _board):
        """ Determines if the player has a pair """
        valid = False
        # find the frequency of all cards held
        frequency = self.numberFrequency(_board)
        # print(sys.getsizeof(frequency))
        # pair is defined if any frequency is exactly equal to 2. Doesn't matter if its greater
        # or if two different values have a frequency of 2
        for value in frequency:
            if value == 2:
                valid = True
        if valid: self.hand = 'pair'
        return valid

    # @timing
    def hasHandTwoPair(self, board):
        """ 
        Determines if the player has a two pair
        Boolean return, does not determine the value of highest two pair 
        """
        #TODO NOT WORKING IN SOME CASES WHERE 2 PAIR IS ON THE BOARD
        valid = False
        frequency = self.numberFrequency(board)
        total = 0
        for value in frequency:
            if value == 2:
                total += 1
        # need exactly two different two pairs
        # possbile to have 3 two pairs, but doesn't matter for this function
        if total == 2:
            valid = True
        if valid: self.hand = 'two_pair'
        return valid
   
    # @timing
    def hasHandThreeOfAKind(self, _board):
        """ 
        Determines if the player has a three of a kind 
        Boolean return, does not determine the value of highest two pair
        """
        valid = False
        frequency = self.numberFrequency(_board)
        # possible to have 2 three of a kinds, but doesn't matter for this function
        for value in frequency:
            if value >= 3:
                valid = True
        if valid: self.hand = 'three_of_a_kind'
        return valid

    # @timing
    def hasHandFlush(self, _board):
        """ 
        Determines if the player has a flush
        Boolean return, does not determine the value of highest flush
        """
        valid = False
        frequency = self.suitFrequency(_board)
        for value in frequency:
            if value >= 5:
                valid = True
        if valid: self.hand = 'flush'
        return valid

    # @timing
    def hasHandStraight(self, _board):
        """ 
        Determines if the player has a straight
        Boolean return, does not determine the value of highest straight
        """
        #NOTE straights cannot wrap around
        valid = False

        frequency = self.numberFrequency(_board)
        # start at the highest value card and iterate down
        count = 0
        for value in reversed(frequency):
            if value >= 1:
                count += 1
                # as soon as count is 5 or greater, stop checking
                if count >= 5:
                    valid = True
                    break
            # if there is no card, set count back to 0 and iterate again for the next lowest ranked card
            else:
                count = 0
    
        if valid: self.hand = 'straight'
        return valid

    # @timing
    def hasHandFullHouse(self, _board):
        """ 
        Determines if the player has a full house
        Boolean return, does not determine the value of the full house
        """
        valid = False
        frequency = self.numberFrequency(_board)
        for i,value in enumerate(frequency):
            # as soon as you get to one that's 2, check the rest if it's equal to 3
            if value == 2:
                # loop through the rest of the array
                for j in range(i+1, 13):
                    if frequency[j] >= 3:
                        valid = True
                        break
            # as soon as you get to one that's 3, check the rest if it's equal to 2
            if value == 3:
                # loop through the rest of the array
                for j in range(i+1, 13):
                    if frequency[j] >= 2:
                        valid = True
                        break        
        if valid: self.hand = 'full_house'
        return valid

    # @timing
    def hasHandFourOfAKind(self, _board):
        """ 
        Determines if the player has a four of a kind
        Boolean return, does not determine the value of the four of a kind
        """
        valid = False
        frequency = self.numberFrequency(_board)
        for value in frequency:
            if value == 4:
                valid = True
        if valid: self.hand = 'four_of_a_kind'
        return valid

    # @timing
    def hasHandStraightFlush(self, _board):
        #NOTE need to know suit and value of current cards considered as you're trying to build the 5 in a row, not the 7 possible
        
        valid = False

        if valid: self.hand = 'straight_flush'
        return valid

    def royalCardValueCheck(self, card):
        if card.value == 'A' or card.value == 'K' or card.value == 'Q' or card.value == 'J' or card.value == "10":
            return True
        else: return False

    # @timing
    # def hasHandRoyalFlush(self, board):
    #     """
    #     Check if the player has a royal flush
    #     """
    #     valid = False
    #     count = 0
    #     suit = None
    #     # check the board
    #     for card in board:
    #         if suit:
    #             if self.royalCardValueCheck(card):
    #                 if card.suit == suit: count += 1
    #                 else: 
    #                     # reset
    #                     suit = card.suit
    #                     count = 1
    #             else: 
    #                 # reset. Only way to get here is if you started building RF, but got a non-royal card
    #                 # need to get the suit 
    #                 # suit = card.suit
    #                 count = 0
    #         else:
    #             if self.royalCardValueCheck(card): 
    #                 count += 1
    #                 suit = card.suit
    #     if self.royalCardValueCheck(self.card1) and self.card1.suit == suit: count += 1
    #     if self.royalCardValueCheck(self.card2) and self.card2.suit == suit: count += 1

        
    #     # if the count is 5, valid
    #     if count >= 5: valid = True

    #     if valid: self.hand = 'royal_flush'
    #     return valid

    # @timing
    def hasHandRoyalFlush(self, board):
        """
        Check if the player has a royal flush
        """
        suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}
        inv_suit_dict = {0: 'c', 1:'s', 2:'d', 3:'h'}
        valid = False 
        count = 0
        suit = None
        rankedBoard = []
        frequency = [0, 0, 0, 0]
        # add on the cards from the board
        for card in board:
            frequency[suit_dict[card.suit]] += 1
        # print(sys.getsizeof(frequency))
        # check the board. Needs to be at least 3 RF cards on the board
        for i, ele in enumerate(frequency):
            if ele >= 3:
                suit = inv_suit_dict[i]
                # sort the board array
                rankedBoard = self.bubbleSort(board)
        for card in reversed(rankedBoard):
            # now have a sorted array. The only way the first card is not a royal card is if there are no royal cards at all 
            if self.royalCardValueCheck(card) and card.suit == suit: count += 1
        if self.royalCardValueCheck(self.card1) and self.card1.suit == suit: count += 1
        if self.royalCardValueCheck(self.card2) and self.card2.suit == suit: count += 1

        # if the count is 5, valid
        if count >= 5: valid = True

        if valid: self.hand = 'royal_flush'
        return valid

    def bubbleSort(self, arr):
        suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}
        value_dict = {'A': 13, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}
        # [lowest ... highest]
        n = len(arr)

        for i in range(n):
            for j in range(0, n-i-1):
                if value_dict[arr[j].value] > value_dict[arr[j+1].value]:
                # and suit_dict[arr[j].suit] > suit_dict[arr[j+1].suit]:
                    # swap
                    arr[j], arr[j+1] = arr[j+1], arr[j]

        return arr

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
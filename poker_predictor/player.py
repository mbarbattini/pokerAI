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

VALUE_DICT_ACE_HIGH = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
VALUE_DICT_ACE_LOW = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}
SUIT_DICT = {'c': 0, 's': 1, 'd': 2, 'h': 3}
INV_SUIT_DICT = {0: 'c', 1:'s', 2:'d', 3:'h'}

class Player:
    
    def __init__(self):
        self.card1 = None
        self.card2 = None
        self.hand = 'high_card'
        self.probability = None
        # an array with 7 elements, worst case is two players have exact same high card up until the last one
        # Player 1: [10,9,8,7,6,5,4]
        # Player 2: [10,9,8,7,6,5,2]
        self.high_card = []
        self.bestCards = []]

    def numberFrequency(self, board, aceHigh=False):
        """ Returns an array of all cards and the number of each currently held by the player """
        frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # cards currently held by the player
        number1 = self.card1.value
        number2 = self.card2.value
        if aceHigh:
            value_dict = VALUE_DICT_ACE_HIGH
        else:
            value_dict = VALUE_DICT_ACE_LOW

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

        # cards currently held by the player
        suit1 = self.card1.suit
        suit2 = self.card2.suit

        frequency[SUIT_DICT[suit1]] += 1
        frequency[SUIT_DICT[suit2]] += 1

        # add on the cards from the board
        for card in board:
            frequency[SUIT_DICT[card.suit]] += 1

        return frequency


    def hasHandPair(self, board):
        """ Determines if the player has a pair """
        valid = False
        frequency = self.numberFrequency(board)
        # pair is defined if any frequency is exactly equal to 2. Doesn't matter if its greater
        # or if two/three different values have a frequency of 2
        for i,value in enumerate(frequency):
            if value == 2:
                valid = True
        if valid: self.hand = 'pair'
        return valid


    def hasHandTwoPair(self, board):
        """ 
        Determines if the player has a two pair 
        """
        valid = False
        frequency = self.numberFrequency(board)
        total = 0
        for value in frequency:
            if value >= 2:
                total += 1
        # need exactly two different two pairs
        # possbile to have 3 two pairs, but doesn't matter for this function
        if total >= 2:
            valid = True
        if valid: self.hand = 'two_pair'
        return valid
   

    def hasHandThreeOfAKind(self, _board):
        """ 
        Determines if the player has a three of a kind 
    
        """
        valid = False
        frequency = self.numberFrequency(_board)
        # possible to have 2 three of a kinds, but doesn't matter for this function
        for value in frequency:
            if value >= 3:
                valid = True
        if valid: self.hand = 'three_of_a_kind'
        return valid


    def hasHandFlush(self, _board):
        """ 
        Determines if the player has a flush
        
        """
        valid = False
        frequency = self.suitFrequency(_board)
        for value in frequency:
            if value >= 5:
                valid = True
        if valid: self.hand = 'flush'
        return valid


    def hasHandStraight(self, board):
        """ 
        Determines if the player has a straight
        1) Check all straight that could begin with an ace
        2) Check all straights that could end with an ace
        """
        #NOTE straights cannot wrap around
        valid = False

        # begin with ace
        frequency = self.numberFrequency(board)
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

        # end with ace
        frequency = self.numberFrequency(board, aceHigh=True)
        count = 0
        for value in reversed(frequency):
            if value >= 1:
                count += 1
                if count >= 5:
                    valid = True
                    break
            else:
                count = 0
    
        if valid: self.hand = 'straight'
        return valid


    def hasHandFullHouse(self, _board):
        """ 
        Determines if the player has a full house
        
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


    def hasHandStraightFlush(self, board):
        """
        Determines if the player has a straight flush
        1) Is there a suit >= 5
        2) Add all cards of that suit to ranked array
        3) Is there a straight len >= 5 among those cards
        """
        valid = False 

        value_dict = VALUE_DICT_ACE_LOW

        # if there is a suit greater than 5
        mostCommonSuit = None
        frequencySuit = [0, 0, 0, 0]
        for card in board:
            frequencySuit[SUIT_DICT[card.suit]] += 1
        frequencySuit[SUIT_DICT[self.card1.suit]] += 1
        frequencySuit[SUIT_DICT[self.card2.suit]] += 1
        for i, ele in enumerate(frequencySuit):
            if ele >= 5:
                mostCommonSuit = INV_SUIT_DICT[i]

        # create a ranked array of only cards of the most common suit
        frequencyValue = [0] * 13
        for card in board:
            if card.suit == mostCommonSuit:
                frequencyValue[value_dict[card.value]] += 1
        if self.card1.suit == mostCommonSuit:
            frequencyValue[value_dict[self.card1.value]] += 1
        if self.card2.suit == mostCommonSuit:
            frequencyValue[value_dict[self.card2.value]] += 1

        # if there is a straight
        count = 0
        for value in reversed(frequencyValue):
            if value >= 1:
                count += 1
                if count >= 5:
                    valid = True
            else:
                count = 0

        if valid: self.hand = 'straight_flush'
        return valid

    def royalCardValueCheck(self, card):
        if card.value == 'A' or card.value == 'K' or card.value == 'Q' or card.value == 'J' or card.value == "10":
            return True
        else: return False


    def hasHandRoyalFlush(self, board):
        """
        Check if the player has a royal flush
        1) Check if the board has at least 3 common suits
        2) Check if the most common suit cards are royal cards
        3) Check if players cards are royal and the same suit
        """
        valid = False 
        count = 0
        mostCommonSuit = None
        frequency = [0, 0, 0, 0]
        # add on the cards from the board
        for card in board:
            frequency[SUIT_DICT[card.suit]] += 1
        # check the board. Needs to be at least 3 RF cards on the board
        for i, ele in enumerate(frequency):
            if ele >= 3:
                mostCommonSuit = INV_SUIT_DICT[i]
                # sort the board array
        for card in reversed(board):
            if self.royalCardValueCheck(card) and card.suit == mostCommonSuit: count += 1
        if self.royalCardValueCheck(self.card1) and self.card1.suit == mostCommonSuit: count += 1
        if self.royalCardValueCheck(self.card2) and self.card2.suit == mostCommonSuit: count += 1

        # if the count is 5, valid
        if count >= 5: valid = True

        if valid: self.hand = 'royal_flush'
        return valid


    # def bestHandHighCard(self, board):
    #     """ Finds the player's 5 cards that make up their best high card hand """
    #     self.bestCards = []

    # def bestHandPair(self, board):
    #     """ Finds the player's 5 cards that make up their best pair """

    #     self.bestCards = []

    # def bestHandTwoPair(self, board):
    #     """ Finds the player's 5 cards that make up their best two pair """
    #     self.bestCards = []

    # def bestHandThreeOfAKind(self, board):
    #     """ Finds the player's 5 cards that make up their best three of a kind """
    #     self.bestCards = []

    # def bestHandStraight(self, board):
    #     """ Finds the player's 5 cards that make up their best straight """
    #     self.bestCards = []

    # def bestHandFlush(self, board):
    #     """ Finds the player's 5 cards that make up their best flush """
    #     self.bestCards = []

    # def bestHandFullHouse(self, board):
    #     """ Finds the player's 5 cards that make up their best full house """
    #     self.bestCards = []

    # def bestHandFourOfAKind(self, board):
    #     """ Finds the player's 5 cards that make up their best four of a kind """
    #     self.bestCards = []

    # def bestHandStraightFlush(self, board):
    #     """ Finds the player's 5 cards that make up their best straight flush """
    #     self.bestCards = []

    # def bestHandRoyalFlush(self, baord):
    #     """ Finds the player's 5 cards that make up their best royal flush """
    #     self.bestCards = []



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
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
        """ Assigns the high_card array in order from best to worst """
        pass

    # TODO(Test the fuck out of this)
    def compareHighCard(self, other):
        """ Compares high card array to another player. Returns winner player object """
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

    def comparePair(self, other):
        """
        Compares two players with a pair. Returns winner player object

        """

        # first compare the value of the hand

        # if the value is the same, move on to high card check
        self.compareHighCard(other)

    def compareTwoPair(self, other):
        """
        Compares two players with a pair. Returns winner player object

        """

        # first compare the value of the hand

        # if the value is the same, move on to high card check
        self.compareHighCard(other)


    def compareThreeOfAKind(self, other):
        """
        Compares two players with a three of a kind. Returns winner player object

        RULES:
        1) Highest three of a kind wins, doesn't matter the suit
        2) If exact same, move on to 2 kicker cards
        """

        # first compare the value of the hand

        # if the value is the same, move on to high card check
        self.compareHighCard(other)

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
        1) Highest flush wins, doesn't matter the suit
        2) If same high card, move on to the next, etc.
        3) If all 5 cards are exactly the same value, split the pot
        """
        pass

    def compareStraight(self, other):
        """
        Compares two players with a straight. Returns winner player object

        RULES:
        Highest straight wins, doesn't matter the suit

        """
        pass

    def compareFourOfAKind(self, other):
        """
        Compares two players with a four a kind. Returns winner player object

        """

        # first compare the value of the hand

        # if the value is the same, move on to high card check
        self.compareHighCard(other)

    #NOTE Probably never will get a scenario where two players both have straight flushes
    def compareStraightFlush(self, other):
        """
        Compares two players with a four a kind. Returns winner player object

        """

        # first compare the value of the hand

        # if the value is the same, move on to high card check
        self.compareHighCard(other)

    #NOTE impossible to get two royal flushes in Texas Hold Em'

    def setHighCardHand(self):
        self.hand = 'high_card'

    def hasHandPair(self, _board):
        """ Determines if the player has a pair """
        valid = False
        # find the frequency of all cards held
        frequency = self.numberFrequency(_board)
        # pair is defined if any frequency is exactly equal to 2. Doesn't matter if its greater
        # or if two different values have a frequency of 2
        for value in frequency:
            if value == 2:
                valid = True
        if valid: self.hand = 'pair'
        return valid

    def hasHandTwoPair(self, _board):
        """ 
        Determines if the player has a two pair
        Boolean return, does not determine the value of highest two pair 
        """
        valid = False
        frequency = self.numberFrequency(_board)
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

    def hasHandThreeOfAKind(self, _board):
        """ 
        Determines if the player has a three of a kind 
        Boolean return, does not determine the value of highest two pair
        """
        valid = False
        frequency = self.numberFrequency(_board)
        # possible to have 2 three of a kinds, but doesn't matter for this function
        for value in frequency:
            if value == 3:
                valid = True
        if valid: self.hand = 'three_of_a_kind'
        return valid

    def hasHandFlush(self, _board):
        """ 
        Determines if the player has a flush
        Boolean return, does not determine the value of highest flush
        """
        valid = False
        frequency = self.suitFrequency(_board)
        for value in frequency:
            if value == 5:
                valid == True
        if valid: self.hand = 'flush'
        return valid

    # TODO(Determining a straight as a set of many numbers and choosing a subset that is in ascending order. Leetcode problem)
    def hasHandStraight(self, _board):
        """ 
        Determines if the player has a straight
        Boolean return, does not determine the value of highest straight
        """
        #NOTE straights cannot wrap around
        valid = False

        if valid: self.hand = 'straight'
        return valid

    def hasHandFullHouse(self, _board):
        """ 
        Determines if the player has a full house
        Boolean return, does not determine the value of the full house
        """
        valid = False
        frequency = self.suitFrequency(_board)
        for i,value in enumerate(frequency):
            # as soon as you get to one that's 2, check the rest if it's equal to 3
            if value == 2:
                # loop through the rest of the array
                for j in range(i+1, len(frequency)):
                    if frequency[j] == 3:
                        valid = True
                        break
            # as soon as you get to one that's 3, check the rest if it's equal to 2
            if value == 3:
                # loop through the rest of the array
                for j in range(i+1, len(frequency)):
                    if frequency[j] == 2:
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
        valid = False

        if valid: self.hand = 'striaght_flush'
        return valid

    def hasHandRoyalFlush(self, _board):
        valid = False
        valueFrequency = self.numberFrequency(_board)
        suitFrequency = self.suitFrequency(_board)
        # ace, king, queen, jack, 10
        if valueFrequency[0] >= 1 and valueFrequency[12] >= 1 and valueFrequency[11] >= 1 and valueFrequency[10] >= 1 and valueFrequency[9] >= 1:
            for value in suitFrequency:
                if value == 5:
                    valid = True

        if valid: self.hand = 'royal_flush'
        return valid

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
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
            if value >= 3:
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
            if value >= 5:
                valid = True
        if valid: self.hand = 'flush'
        return valid

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
                for j in range(i+1, len(frequency)):
                    if frequency[j] >= 3:
                        valid = True
                        break
            # as soon as you get to one that's 3, check the rest if it's equal to 2
            if value == 3:
                # loop through the rest of the array
                for j in range(i+1, len(frequency)):
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

    def hasHandStraightFlush(self, _board):
        #NOTE need to know suit and value of current cards considered as you're trying to build the 5 in a row, not the 7 possible
        
        valid = False

        if valid: self.hand = 'straight_flush'
        return valid

    def hasHandRoyalFlush(self, _board):
        valid = False
        valueFrequency = self.numberFrequency(_board)
        suitFrequency = self.suitFrequency(_board)
        # ace, king, queen, jack, 10
        if valueFrequency[0] >= 1 and valueFrequency[12] >= 1 and valueFrequency[11] >= 1 and valueFrequency[10] >= 1 and valueFrequency[9] >= 1:
            #TODO NOT WORKING there can be a scenario where you have a royal straight, but the flush includes the 1 or 2 other cards
            for value in suitFrequency:
                if value >= 5:
                    valid = True
                    # print("Royal Flush!")
                    # print(f"{self.card1}{self.card2}")

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
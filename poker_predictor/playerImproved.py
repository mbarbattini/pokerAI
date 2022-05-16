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
        self.bestCards = []

    def hasHandPair(self, board):
        """ 
        Determines if the player has a pair
        1) Find all valid combinations of 2 cards
        2) Determine best hand for each valid combination
        3) Compare value of high card
        4) Compare 3 kicker cards
        """
        valid = False
        cards = [self.card1, self.card2] + board
        totalCards = len(cards)
        # form all combinations of 2 cards
        combinations = []
        for i in range(totalCards):
            for j in range(i+1, totalCards):
                combinations.append([cards[i],cards[j]])
        # delete invalid pairs
        for i in range(len(combinations)):
            if not combinations[0][0].value == combinations[0][1].value:
               del combinations[0]
        return valid

    def hasHandTwoPair(self, board):
        valid = False
        return valid

    def hasHandThreeOfAKind(self, board):
        valid = False
        return valid

    def hasHandStraight(self, board):
        valid = False
        return valid

    def hasHandFlush(self, board):
        valid = False
        return valid

    def hasHandFullHouse(self, board):
        valid = False
        return valid

    def hasHandFourOfAKind(self, board):
        valid = False
        return valid

    def hasHandStraightFlush(self, board):
        valid = False
        return valid

    def hasHandRoyalFlush(self, board):
        valid = False
        return valid
VALUE_DICT_ACE_HIGH = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
VALUE_DICT_ACE_LOW = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}
# SUIT_DICT = {'c': 0, 's': 1, 'd': 2, 'h': 3}
# INV_SUIT_DICT = {0: 'c', 1:'s', 2:'d', 3:'h'}
STRAIGHT_STRING_ACE_LOW = 'K Q J 10 9 8 7 6 5 4 3 2 A'
STRAIGHT_STRING_ACE_HIGH = 'A K Q J 10 9 8 7 6 5 4 3 2'

"""
Tiebreaker member variable is an array with variable size. Depends on what hand the players has.
    For a pair, it is size 4 and contains [value of pair, high card 1, high card 2, high card 3]
    For a full house, it is size 2 and contains [value of three of a kind, value of pair]
    This is okay because the program only compares the tiebreaker between two players when they have the same hand.
    There is no need to compare the tiebreaker for a player with a full house and a pair,
    so there is no problems with different sizes of the arrays between players. 
"""

class Player:
    
    def __init__(self, _number):
        self.card1 = None
        self.card2 = None
        self.hand = 'high_card'
        self.probability = None
        self.tiebreaker = None
        self.bestHand = []
        self.number = _number
        self.bet = None
        self.networth = 100.0
        self.user = False
        self.out = False

    def printHand(self):
        print("           ", end=' ')
        for card in self.bestHand:
            print(f"{card.value}{card.suit}",end=' ')


    def setHighCardTiebreaker(self, board):
        """
        Sets the player's tiebreaker to their best 5 cards.
        Only called when the player only has a high card
        """
        cards = [self.card1, self.card2] + board
        cards = sorted(cards, key=lambda card: (VALUE_DICT_ACE_HIGH[card.value]), reverse=True)
        self.tiebreaker = [card.value for card in cards[:5]]


    def hasHandPair(self, board):
        """
        Determines if the player has a pair. 
        Tiebreaker: 
            [Value of pair, kicker 1, kicker 2, kicker 3]
        """
        cards = [self.card1, self.card2] + board
        # get the value of each card held
        allValues = [value for value,suit in cards]
        # get the unique values
        uniqueValues = set(allValues)
        pairs = [v for v in uniqueValues if allValues.count(v) == 2]
        if len(pairs) != 1:
            return False
        self.hand = 'pair'
        # don't double count the value of the pair in the tiebreaker
        uniqueValues.remove(pairs[0])
        highCards = sorted(uniqueValues, key=lambda f: (VALUE_DICT_ACE_HIGH[f]), reverse=True)
        # only three high cards for a pair
        highCards = highCards[:3]
        self.tiebreaker = pairs + highCards
        self.bestHand = [card for card in cards if card.value == pairs[0] or card.value in highCards]
        return True

    def hasHandTwoPair(self, board):
        """
        Determines if the player has a two pair.
        Tiebreaker:
            [value of highest pair, value of second highest pair, kicker]
        """
        cards = [self.card1, self.card2] + board
        allValues = [value for value,suit in cards]
        uniqueValues = set(allValues)
        pairs = [v for v in uniqueValues if allValues.count(v) == 2]
        # accounts for 3 two pairs
        if len(pairs) < 2:
            return False
        # sort pairs to get the best 2
        pairs = sorted(pairs, key=lambda f: (VALUE_DICT_ACE_HIGH[f]), reverse=True)
        pairs = pairs[:2]
        # remove the highest two pairs from all unique cards
        uniqueValues.remove(pairs[0])
        uniqueValues.remove(pairs[1])
        highCards = sorted(uniqueValues, key=lambda f: (VALUE_DICT_ACE_HIGH[f]), reverse=True)
        kicker = highCards[0]
        self.hand = 'two_pair'
        self.tiebreaker = pairs + [kicker]
        self.bestHand = [card for card in cards if card.value in pairs or card.value == kicker]
        return True

    def hasHandThreeOfAKind(self, board):
        """
        Determines if the player has a three of a kind.
        Tiebreaker:
            [value of three of a kind, kicker 1, kicker 2]
        """
        cards = [self.card1, self.card2] + board
        allValues = [value for value,suit in cards]
        uniqueValues = set(allValues)
        threes = [v for v in uniqueValues if allValues.count(v) == 3]
        # accounts for 2 three of a kinds
        if len(threes) < 1:
            return False
        threes = sorted(threes, key=lambda f: (VALUE_DICT_ACE_HIGH[f]), reverse=True)
        bestThree = threes[0]
        uniqueValues.remove(threes[0])
        highCards = sorted(uniqueValues, key=lambda f: (VALUE_DICT_ACE_HIGH[f]), reverse=True)
        kickers = highCards[:2]
        self.hand = 'three_of_a_kind'
        self.tiebreaker = [bestThree] + kickers
        self.bestHand = [card for card in cards if card.value == bestThree or card.value in kickers]
        return True

    def hasHandStraight(self, board):
        """
        Determines if the player has a straight
        Tiebreaker:
            [highest card of straight]
        """
        #TODO ties not working when straight is on the board but other players have a higher straight with one extra card
        cards = [self.card1, self.card2] + board
        # consider straights that begin with ace 
        ranking, straightString = VALUE_DICT_ACE_LOW, STRAIGHT_STRING_ACE_LOW
        # remove any duplicate cards that would otherwise interrupt a straight
        allValues = [value for value,suit in cards]
        uniqueValues = list(set(allValues))
        ordered = sorted(uniqueValues, key=lambda v: ranking[v], reverse=True)
        # accounts for 3 possible ways to pick a 5 straight out of 7 ordered cards
        # or only one way to pick a 5 straight out of 5 ordered cards
        for i in range(len(ordered) - 4):
            # if the substring is in the full string
            substring = ' '.join(value for value in ordered[i:i+5])
            if substring in straightString:
                self.hand = 'straight'
                self.tiebreaker = [ordered[i]]
                self.bestHand = [card for card in cards if card.value in ordered[i:i+5]]
                return True

        # consider straights with ace high
        # since checked all others first, this can only return an Ace high straight
        ranking, straightString = VALUE_DICT_ACE_HIGH, STRAIGHT_STRING_ACE_HIGH
        ordered = sorted(uniqueValues, key=lambda v: ranking[v], reverse=True)
        substring = ' '.join(value for value in ordered[:5])
        if substring in straightString:
            self.hand = 'straight'
            self.tiebreaker = ['A']
            self.bestHand = [card for card in cards if card.value in ordered[:5]]
            return True
        return False




    def hasHandFlush(self, board):
        """
        Determines if the player has a flush
        Tiebreaker:
            [value of highest card in the flush]
        """
        cards = [self.card1, self.card2] + board
        allSuits = [suit for value,suit in cards]
        uniqueSuit = set(allSuits)
        flushSuit = [s for s in uniqueSuit if allSuits.count(s) >= 5]
        if len(flushSuit) == 0:
            return False
        flushSuit = flushSuit[0]
        # get all the cards in the flush suit
        flushCards = [card for card in cards if card.suit == flushSuit]
        # sort and get the best 5
        flushCards = sorted(flushCards, key=lambda card: VALUE_DICT_ACE_HIGH[card.value], reverse=True)
        self.hand = 'flush'
        self.tiebreaker = [card.value for card in flushCards[:5]]
        self.bestHand = flushCards[:5]
        return True

    def hasHandFullHouse(self, board):
        """
        Determines if the player has a full house
        Tiebreaker:
            [value of 3 of a kind, value of pair]
        """
        cards = [self.card1, self.card2] + board
        allValues = [value for value,suit in cards]
        uniqueValues = set(allValues)
        tiebreaker = []
        if len(uniqueValues) > 4:
            return False
        for ele1 in uniqueValues:
            if allValues.count(ele1) == 3:
                for ele2 in uniqueValues:
                    if allValues.count(ele2) == 2:
                        tiebreaker = [ele1, ele2]
                        self.hand = 'full_house'
                        self.tiebreaker = tiebreaker
                        self.bestHand = [card for card in cards if card.value in [ele1, ele2]]
                        return True
            if allValues.count(ele1) == 2:
                for ele2 in uniqueValues:
                    if allValues.count(ele2) == 3:
                        tiebreaker = [ele2, ele1]
                        self.hand = 'full_house'
                        self.tiebreaker = tiebreaker
                        self.bestHand = [card for card in cards if card.value in [ele1, ele2]]
                        return True
        return False

    def hasHandFourOfAKind(self, board):
        """
        Determines if the player has a four of a kind.
        Tiebreaker:
            [value of four of a kind]
        """
        cards = [self.card1, self.card2] + board
        allValues = [value for value,suit in cards]
        uniqueValues = set(allValues)
        fours = [v for v in uniqueValues if allValues.count(v) == 4]
        if not fours:
            return False
        uniqueValues.remove(fours[0])
        ordered = sorted(uniqueValues, key=lambda v: VALUE_DICT_ACE_HIGH[v], reverse=True)
        kicker = ordered[0]
        self.hand = 'four_of_a_kind'
        self.tiebreaker = fours + [kicker]
        
        #NOTE does not give 5 cards when kicker card has a frequency of greater than 2
        self.bestHand = [card for card in cards if card.value == fours[0] or card.value == kicker]
        return True
        

    def hasHandStraightFlush(self, board):
        """
        Determines if the player has a straight flush
        Tiebreaker:
            [highest card of straight]
        """
        cards = [self.card1, self.card2] + board
        allSuits = [suit for value,suit in cards]
        uniqueSuit = set(allSuits)
        mostCommonSuit = [s for s in uniqueSuit if allSuits.count(s) >= 5]
        if len(mostCommonSuit) == 0:
            return False

        # consider only those with ace low
        ranking, straightString = VALUE_DICT_ACE_LOW, STRAIGHT_STRING_ACE_LOW
        ordered = sorted(cards, key=lambda card: (ranking[card.value], card.suit), reverse=True)
        ordered = [card for card in ordered if card.suit == mostCommonSuit[0]]
        for i in range(len(ordered) - 4):
            values = [card.value for card in ordered[i:i+5]]
            substring = ' '.join(values)
            if substring in straightString:
                self.hand = 'straight_flush'
                self.tiebreaker = [ordered[i].value]
                self.bestHand = [card for card in cards if card.value in values and card.suit == mostCommonSuit[0]]
                return True

    def hasHandRoyalFlush(self, board):
        """
        Determines if the player has a royal flush
        Tiebreaker:
            N/A
        """
        cards = [self.card1, self.card2] + board
        royalFlushString = 'A K Q J 10'
        allSuits = [suit for value,suit in cards]
        uniqueSuit = set(allSuits)
        mostCommonSuit = [s for s in uniqueSuit if allSuits.count(s) >= 5]
        if len(mostCommonSuit) == 0:
            return False
        ordered = sorted(cards, key=lambda card: (VALUE_DICT_ACE_HIGH[card.value], card.suit), reverse=True)
        # remove duplicate cards of not the > 5 suit
        ordered = [card for card in ordered if card.suit == mostCommonSuit[0]]
        values = [card.value for card in ordered[:5]]
        substring = ' '.join(values)
        if substring in royalFlushString:
            self.hand = 'royal_flush'
            self.tiebreaker = []
            self.bestHand = [card for card in cards if card.value in values and card.suit == mostCommonSuit[0]]
            return True
        return False
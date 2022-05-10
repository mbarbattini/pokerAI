# # always want to rank ace as the highest, only consider it being lowest in ex. determine straight method
# import numpy as np
# from dataclasses import dataclass
# import sys
# from functools import wraps
# from time import perf_counter, time

# @dataclass
# class Card:
#     value: str
#     suit: str

# def timing(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         start = perf_counter()
#         result = f(*args, **kwargs)
#         end = perf_counter()
#         print(f'{(end-start)*1e6} us\n')
#         return result
#     return wrapper

# value_rankings = {
#     '2': 1,
#     '3': 2,
#     '4': 3,
#     '5': 4,
#     '6': 5,
#     '7': 6,
#     '8': 7,
#     '9': 8,
#     '10': 9,
#     'J': 10,
#     'Q': 11,
#     'K': 12,
#     'A': 13
# }

# class Player:
    
#     def __init__(self):
#         self.card1 = None
#         self.card2 = None
#         self.hand = "high_card"
#         self.probability = None
#         # an array with 7 elements, worst case is two players have exact same high card up until the last one
#         # Player 1: [10,9,8,7,6,5,4]
#         # Player 2: [10,9,8,7,6,5,2]
#         self.high_card = []
#         self.cardArray = None

#     @timing
#     def buildPlayerHandArray(self, board, aceHigh=False):
#         """
#         Creates a 2D array of shape (13, 4) of all possible cards ranked from worst to best (lowest index -> highest index)
#         """
#         suit_dict = {'c': 0, 's': 1, 'd': 2, 'h': 3}
#         value_dict = None
#         if aceHigh:
#             value_dict = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
#         else:
#             value_dict = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}

#         localBoard = np.append(board, [self.card1,self.card2])

#         cardsArr = np.empty((13,4), dtype=Card)
#         for card in localBoard:
#             indexValue = value_dict[card.value]
#             indexSuit = suit_dict[card.suit]
#             cardsArr[indexValue,indexSuit] = card

#         self.cardArray = cardsArr

#     def setHighCard(self):
#         """ Assigns the high_card array in order from best to worst """
#         pass
    
#     def setHighCardHand(self):
#         self.hand = 'high_card'

#     @timing
#     def hasHandPair(self):
#         """ Determines if the player has a pair """
        
#         # self.buildPlayerHandArray(board)
#         for i in range(13):
#             if np.count_nonzero(self.cardArray[i,:]) >= 2:
#                 self.hand = 'pair'
#                 return True
#         return False

#     @timing
#     def hasHandTwoPair(self):
#         """ Determines if the player has a two pair """
#         # self.buildPlayerHandArray(board)
#         count = 0
#         for i in range(13):
#             if np.count_nonzero(self.cardArray[i,:]) == 2:
#                 count += 1
#                 if count >= 2:
#                     self.hand = 'two_pair'
#                     return True
#         return False

#     @timing
#     def hasHandThreeOfAKind(self):
#         """  Determines if the player has a three of a kind """
#         # self.buildPlayerHandArray(board)
#         for i in range(13):
#             if np.count_nonzero(self.cardArray[i,:]) >= 3:
#                 self.hand = 'three_of_a_kind'
#                 return True
#         return False

#     @timing
#     def hasHandFlush(self):
#         """ Determines if the player has a flush """
#         # self.buildPlayerHandArray(board)
#         for i in range(4):
#             if np.count_nonzero(self.cardArray[:,i]) >= 5:
#                 self.hand = 'flush'
#                 return True
#         return False

#     @timing
#     def hasHandStraight(self):
#         """ Determines if the player has a straight """
#         # self.buildPlayerHandArray(board)
#         for i in range(13):
#             count = 0
#             if np.count_nonzero(self.cardArray[i,:]) >= 1:
#                 count += 1
#                 if count >= 5:
#                     #TODO somehow get the highest card of the straight
#                     self.hand = 'straight'
#                     return True
#             else:
#                 count = 0
#         return False

#     @timing
#     def hasHandFullHouse(self):
#         """ Determines if the player has a full house """
#         # self.buildPlayerHandArray(board)
#         valid = False
#         for i in range(13):
#             if np.count_nonzero(self.cardArray[i,:]) == 3:
#                 # loop through the rest
#                 for j in range(i+1,13):
#                     if np.count_nonzero(self.cardArray[j,:]) >= 2:
#                         valid = True
#             elif np.count_nonzero(self.cardArray[i,:]) == 2:
#                 for j in range(i+1,13):
#                     if np.count_nonzero(self.cardArray[j,:]) >= 3:
#                         valid = True
#             if valid:
#                 self.hand = 'full_house'
#                 return True
#         return False

#     @timing
#     def hasHandFourOfAKind(self):
#         """ Determines if the player has a four of a kind """
#         # self.buildPlayerHandArray(board)
#         for i in range(13):
#             if np.count_nonzero(self.cardArray[i,:]) == 4:
#                 self.hand = 'four_of_a_kind'
#                 return True
#         return False
    
#     @timing
#     def hasHandStraightFlush(self):
#         """" Check if the player has a straight flush """
#         # self.buildPlayerHandArray(board)
#         # iterate through each suit array and try to find successive entries
#         for i in range(4):
#             count = 0
#             # get all cards of a single suit
#             for card in self.cardArray[:,i]:
#                 # if there is a card, add to count
#                 if card:
#                     count += 1
#                     # as soon as count is 5, successful
#                     if count >= 5:
#                         self.hand = 'straight_flush'
#                         return True
#                 else:
#                     count = 0
#         return False

#     @timing
#     def hasHandRoyalFlush(self, board):
#         """ Determines if the player has a royal flush """
#         self.buildPlayerHandArray(board, aceHigh=True)
#         # print(sys.getsizeof(self.card1))
#         # print(sys.getsizeof(self.cardArray))
#         for i in range(4):
#             # get all royal cards of a single suit
#             if np.count_nonzero(self.cardArray[-5:,i]) >= 5:
#                 self.hand = 'royal_flush'
#                 return True
#         return False

#     def evaluateFullHouse(self, board):
#         """ Determines the chances of the player getting a full house on the next sequence """
#         outcome = 0
#         for ele in self.numberFrequency():
#             if ele == 2:
#                 # when 
#                 pass
#             if ele == 3:
#                 #
#                 pass

#         return outcome
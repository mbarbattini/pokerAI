class Betting:
    def __init__(self, _littleBlindAmount):
        self.currentBetAmount = _littleBlindAmount * 2
        self.betMade = False
        self.pot = 0.0


    def makeBet(self, _player, _betAmount):
        if _betAmount > _player.networth:
            print("Bet too large!")
            return False
        elif _betAmount < self.currentBetAmount:
            print("Bet must be larger than the current bet.")
            return False
        else:
            _player.networth -= _betAmount
            self.currentBetAmount = _betAmount
            self.pot += _betAmount
            self.betMade = True
            return True
            


    def allIn(self, _player):
        self.pot += _player.networth
        _player.networth = 0


    def callBet(self, _player):
        if self.currentBetAmount > _player.networth:
            return False
        else:
            _player.networth -= self.currentBetAmount
            self.pot += self.currentBetAmount
            self.betMade = True
            return True


    def collectAnte(self, _littleBlindValue, _players, _dealerIndex):
        bigBlind = _littleBlindValue * 2
        self.currentBetAmount = bigBlind

        orderedPlayers = _players[_dealerIndex:] + _players[:_dealerIndex]

        # dealer ante
        if orderedPlayers[0].networth < bigBlind:
            orderedPlayers[0].out = True
        else:
            orderedPlayers[0].networth -= bigBlind

        # little blind ante
        if orderedPlayers[1].networth < _littleBlindValue:
            orderedPlayers[1].out = True
        else:
           orderedPlayers[1].networth -= _littleBlindValue
        
        # big blind ante
        if orderedPlayers[2].networth < bigBlind:
            orderedPlayers[2].out = True
        else:
            orderedPlayers[2].networth -= bigBlind
        
        # rest of the players ante
        for player in orderedPlayers[3:]:
            if player.networth < bigBlind:
                player.out = True
            else:
                player.networth -= bigBlind
# Parent class for creating player controllers to be used in 
# a nim game.
class playerController:
    def __init__(self, name, rank, callback):
        self.name = name
        self.rank = rank
        self.callback = callback

    def getName(self):
        return self.name
    
    # Legacy for finding which turn the controller plays
    # now unused.
    def getRank(self):
        return self.rank

    def decrementRank(self):
        self.rank -= 1

    # Shell method with takes a callback. Used for overriding.
    def playTurn(self, nim_instance):
        self.callback(self.name, nim_instance)
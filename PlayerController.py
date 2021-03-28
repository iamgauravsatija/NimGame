class playerController:
    def __init__(self, name, rank, callback):
        self.name = name
        self.rank = rank
        self.callback = callback

    def getName(self):
        return self.name
    
    def getRank(self):
        return self.rank

    def decrementRank(self):
        self.rank -= 1

    def playTurn(self, nim_instance):
        self.callback(self.name, nim_instance)
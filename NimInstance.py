class NimInstance:
    def __init__(self, pile_list, wincon_list, is_misere=True):
        self.pile_list = pile_list
        self.wincon_list = wincon_list
        for rule in self.wincon_list:
            rule.sort()
        self.is_misere = is_misere

    # Takes (amount) objects from (pile_num) pile in 
    # an authorized manner.
    def takeFromPile(self, pile_num, amount):
        if pile_num >= len(self.pile_list):
            return
        
        if amount < self.pile_list[pile_num]:
            self.pile_list[pile_num] -= amount

        else:
            self.pile_list.pop(pile_num) 

    # Returns true if a win/lose condition is found.
    # Whether this results in a win or lose for player
    # is controlled by the game controller. Not this object.
    def checkForWin(self):
        return self.stateIsWin(self.pile_list)

    # Returns true if the given state would result in termination
    def stateIsWin(self, game_state):
        game_state = sorted(game_state)

        for wincon in self.wincon_list:
            if game_state == wincon:
                return True

        return False

    # Returns a copy of the pile list. This copy may be viewed
    # and/or altered without altering this object's list.
    def peek_list(self):
        return self.pile_list.copy()

    # Game setting. Used to determine win/lose conditions.
    def isMisere(self):
        return self.is_misere

    # Creates a copy of the instance. Currently unused.
    def copy(self):
        return NimInstance(self.pile_list.copy(), self.wincon_list)

    def peekAfterTurn(self, pile_index, amount):
        result = self.copy()
        result.takeFromPile(pile_index, amount)
        return result

        
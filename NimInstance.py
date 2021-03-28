class NimInstance:
    def __init__(self, pile_list, wincon_list, is_misere=True):
        self.pile_list = pile_list
        self.wincon_list = wincon_list
        self.is_misere = is_misere

    def takeFromPile(self, pile_num, amount):
        if pile_num >= len(self.pile_list):
            return
        
        if amount < self.pile_list[pile_num]:
            self.pile_list[pile_num] -= amount

        else:
            self.pile_list.pop(pile_num) 

    def checkForWin(self):
        temp = sorted(self.pile_list)

        for wincon in self.wincon_list:
            if temp == wincon:
                return True

        return False

    def peek_list(self):
        return self.pile_list.copy()

    def isMisere(self):
        return self.is_misere

    def copy(self):
        return NimInstance(self.pile_list.copy(), self.wincon_list)

        
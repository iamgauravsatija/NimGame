import random

from PlayerController import playerController

# Simple bot that randomly picks a pile and amount
#to take from said pile.
class randomBot(playerController):

    @staticmethod
    def getDescription():
        return "a random selection bot"

    def playTurn(self, nim_instance):
        pile_list = nim_instance.peek_list()
        index = random.randrange(0, len(pile_list))
        amount = random.randint(1, pile_list[index])

        self.callback(self.name, nim_instance, (index, amount))

# Bot designed to always win a 1v1 in a game with only the
# first win condition whenever possible.    
class standard1v1Bot(playerController):

    @staticmethod
    def getDescription():
        return "a standard 1v1 bot"

    def playTurn(self, nim_instance):
        if(nim_instance.isMisere()):
            choice = self.getMisereChoice(nim_instance.peek_list())
        else:
            choice = self.getStandardChoice(nim_instance.peek_list())

        self.callback(self.name, nim_instance, choice)

    # If playing a standard game, bot will use this method to find its next move.
    def getStandardChoice(self, pile_list):
        nim_sum = 0

        for pile in pile_list:
            nim_sum = nim_sum ^ pile

        largest_pile = 0
        saved_index = 0

        for i, pile in enumerate(pile_list):
            if nim_sum ^ pile < pile:
                return (i, pile-(nim_sum^pile))
            else:
                if pile > largest_pile:
                    largest_pile = pile
                    saved_index = i
        
        return (saved_index, 1)

    # If playing a misere game, bot will use this method to find its next choice.
    def getMisereChoice(self, pile_list):
        large_piles = 0
        small_piles = 0

        for i, pile in enumerate(pile_list):
            if pile > 1:
                large_piles += 1
                saved_index = i
            else:
                small_piles += 1

        if large_piles == 1:
            if small_piles%2 == 1:
                return (saved_index, pile_list[saved_index])
            else:
                return (saved_index, pile_list[saved_index]-1)

        else:
            return self.getStandardChoice(pile_list)
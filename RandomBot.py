import random

from PlayerController import playerController

# Simple bot that randomly picks a pile and amount
#to take from said pile.
class randomBot(playerController):

    def playTurn(self, nim_instance):
        pile_list = nim_instance.peek_list()
        index = random.randrange(0, len(pile_list))
        amount = random.randint(1, pile_list[index])

        self.callback(self.name, nim_instance, (index, amount))